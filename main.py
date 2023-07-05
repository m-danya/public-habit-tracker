import sys

from aiogram import executor
from loguru import logger
from pht.bot import dp, scheduler
import pht.models  # noqa

import pht.routes.commands  # noqa, must be at the beginning
import pht.routes.onboarding  # noqa
import pht.routes.my_habits  # noqa
import pht.routes.add_new_habit  # noqa
import pht.ask_about_day  # noqa
import pht.routes.settings
import pht.routes.menu  # noqa, must be imported by the last of routes

import pht.routes.errors  # noqa

from pht.models import User

# remove default logger and add a nice one
logger.remove()
logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)

if __name__ == "__main__":
    scheduler.start()
    logger.info("Starting a bot")
    for user in User.select():
        if not user.scheduler_job_exists():
            user.set_up_scheduler_job()
            logger.warning(
                f"Scheduler job for {user} was not found. It was set up again."
            )
    executor.start_polling(dp, skip_updates=True)
