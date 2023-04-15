from datetime import datetime

from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.postgres_ext import JSONField

from pht.bot import config

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
    username = CharField()
    full_name = CharField()
    created_at = DateTimeField(default=ts_default)
    rating_privacy = CharField(default="private")  # 'public'
    time_to_ask = CharField(default="22:00")  # '22:00'

    def __repr__(self):
        return f"<User: {self.username} / {self.full_name}>"

    def __str__(self):
        return self.__repr__()


class Habit(BaseModel):
    owner = ForeignKeyField(User, backref="habits")
    name = CharField()
    answer_type = CharField()  # 'bool' or 'integer'
    regularity = JSONField()
    created_at = DateTimeField(default=ts_default)


class Answer(BaseModel):
    habit = ForeignKeyField(Habit, backref="answers")
    content = IntegerField()
    description = CharField()  # "valid_reason" or other explanation
    date = DateTimeField(default=ts_default)
    changed_at = DateTimeField(default=ts_default)


class Event(BaseModel):
    ts = DateTimeField(default=ts_default)
    type = CharField()
    data = JSONField()


with db:
    db.drop_tables([User, Habit, Event])  # FIXME: only for initial development
    db.create_tables([User, Habit, Event])
