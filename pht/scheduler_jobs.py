"""
This module contains functions that are used as jobs for APScheduler,
 i.e. they are called by trigger when needed (e.g. every day at specific time)

One should not use Peewee models classes as arguments for scheduler jobs, because
arguments for jobs are serialized at the moment of adding a job to scheduler and
this serialized data is stored inside Redis. In case of using Peewee model as
an argument for job, the serialized data will quickly become inconsistent with
actual User object, which will lead to data loss. Summing up, one should use
object id as an argument for a scheduler job.
"""

from pht.data import Texts
from pht.models import Habit, User
from pht.utils import send_message


async def ask_about_day_job(user_id):
    user = User.get_by_id(user_id)
    await send_message(user.id, Texts.ask_about_day(n=len(user.habits)))
