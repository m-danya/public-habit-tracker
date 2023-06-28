from dataclasses import dataclass
from datetime import time, datetime, timedelta, timezone, date
from loguru import logger
from typing import Optional

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.postgres_ext import JSONField

from pht.bot import config, scheduler
from pht.data import SCHEDULER_FORGET_IF_MISSED_SECONDS, IntegerInputRequired
from pht.utils import days_left_till_sunday, get_nearest_monday, get_nearest_sunday

db = PooledPostgresqlExtDatabase(
    config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    max_connections=8,
    stale_timeout=300,
)

ts_default = datetime.utcnow


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    # id, the primary key, is equal to `message.from_id`
    id: str = CharField(primary_key=True)
    username: str = CharField()
    full_name: str = CharField()
    created_at: datetime = DateTimeField(default=ts_default)
    rating_publicity: bool = BooleanField(default=True)  # 'public'
    time_to_ask: time = TimeField(
        default=time(hour=19, minute=0)
    )  # '22:00' in UTC+3:00
    scheduler_job_id: Optional[str] = CharField(default="")

    def __repr__(self):
        return f"<User: {self.username} / {self.full_name}>"

    def __str__(self):
        return self.__repr__()

    def _get_cron_trigger(self):
        # FIXME: development/debugging purposes only
        # return IntervalTrigger(seconds=30)

        # every day at hh:mm
        return CronTrigger(
            hour=self.time_to_ask.hour, minute=self.time_to_ask.minute, timezone="utc"
        )

    def set_up_scheduler_job(self):
        scheduler_job_id = f"user_{self.id}_scheduler"
        from pht.ask_about_day import ask_about_day_job

        scheduler.add_job(
            ask_about_day_job,
            trigger=self._get_cron_trigger(),
            args=(self.id,),
            misfire_grace_time=SCHEDULER_FORGET_IF_MISSED_SECONDS,
            id=scheduler_job_id,
            replace_existing=True,
        )

        self.scheduler_job_id = scheduler_job_id
        self.save()

        logger.debug(f"Job {self.scheduler_job_id} set up to {self.time_to_ask}")

    def reschedule_scheduler_job(self):
        """
        This method should be called when `User.time_to_ask` is changed
        """
        scheduler.reschedule_job(
            self.scheduler_job_id, trigger=self._get_cron_trigger()
        )

        logger.debug(f"{self.scheduler_job_id} was rescheduled to {self.time_to_ask}")

    def remove_scheduler_job(self):
        if self.scheduler_job_id:
            scheduler.remove_job(self.scheduler_job_id)


@dataclass
class HabitStatus:
    # Status of habit for a given day
    emoji: str
    value: int


class Habit(BaseModel):
    owner: User = ForeignKeyField(User, backref="habits", on_delete="CASCADE")
    name: str = CharField()
    answer_type: str = CharField()  # 'bool' or 'integer'
    regularity: int = IntegerField()  # 3 (times a week)
    created_at: datetime = DateTimeField(default=ts_default)

    def __repr__(self):
        return f"<Habit: {self.name}, {self.answer_type}, {self.regularity}, owner: {self.owner}>"

    def __str__(self):
        return self.__repr__()

    def get_status_for_day(self, day: date, empty_emoji="") -> HabitStatus:
        """
        Retuns a status for a given day.

        ✅: completed (it can be both "yes" or "10 minutes")
        ❎: failed, but it can be (or could be) catched up till the end of the
        week (or the plan for this week is already finished)
        ❌: failed, can't catch up
        empty: habit didn't exist at that day

        Day can be arbitrary, from any week, not just current.
        """
        if day < self.created_at.date():
            return HabitStatus(empty_emoji, 0)
        answer = Answer.get_or_none(habit=self, date=day)
        if answer and answer.value:
            return HabitStatus("✅", answer.value)

        days_completed = 0

        for answer in Answer.from_monday_to_day(day, self):
            if answer.value:
                days_completed += 1

        need_to_succeed_times = self.regularity - days_completed
        if days_left_till_sunday(day) >= need_to_succeed_times:
            return HabitStatus("❎", 0)
        else:
            return HabitStatus("❌", 0)

    @property
    def type_emoji(self):
        return "⏱️" if self.answer_type == "integer" else "🎯"


class Answer(BaseModel):
    habit: Habit = ForeignKeyField(Habit, backref="answers")
    value: int = IntegerField()  # 0/1 or 0/int
    date: date = DateField()
    changed_at: datetime = DateTimeField(default=ts_default)

    @classmethod
    def from_monday_to_day(cls, day: date, habit: Habit):
        """
        Get all answers from Monday to given date.

        Example: if given date is 21.06, returns all answers for given habit
        from 19.06 to 21.06
        """
        from_date = get_nearest_monday(day)
        to_date = day
        return Answer.select().where(
            habit == habit & Answer.date >= from_date & Answer.date <= to_date
        )

    @classmethod
    def toggle(cls, habit: Habit, day: date):
        """
        Respond to an event of toggling habit's button in `ask_about_day`

        If there is no Answer for given `habit` and `day`, then create it. If
        there is an existing answer, change it's value to an opposite one.
        """
        answer = Answer.get_or_none(habit=habit, date=day)
        if answer:
            if answer.value:
                answer.value = 0
                answer.save()
            else:
                if habit.answer_type == "bool":
                    answer.value = 1
                    answer.save()
                elif habit.answer_type == "integer":
                    raise IntegerInputRequired
                else:
                    raise RuntimeError
        else:
            if habit.answer_type == "integer":
                raise IntegerInputRequired
                return
            if habit.answer_type != "bool":
                raise RuntimeError

            Answer.create(habit=habit, value=1, date=day)

    @classmethod
    def set_integer_value(cls, habit: Habit, day: date, value: int):
        answer = Answer.get_or_none(habit=habit, date=day)
        if answer:
            answer.value = value
            answer.save()
        else:
            Answer.create(habit=habit, value=value, date=day)


class Event(BaseModel):
    ts: datetime = DateTimeField(default=ts_default)
    type: str = CharField()
    data: dict = JSONField()


with db:
    db.create_tables([User, Habit, Answer, Event])
