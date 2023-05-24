import sys

from aiogram import executor
from loguru import logger
from pht.bot import dp, scheduler
import pht.models  # noqa

import pht.routes.commands  # noqa, must be at the beginning
import pht.routes.onboarding  # noqa
import pht.routes.my_habits  # noqa
import pht.routes.add_new_habit  # noqa
import pht.routes.settings
import pht.routes.menu  # noqa, must be imported by the last of routes
import pht.routes.errors  # noqa

# remove default logger and add a nice one
logger.remove()
logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)

if __name__ == "__main__":
    scheduler.start()
    logger.info("Starting a bot")
    executor.start_polling(dp, skip_updates=True)
