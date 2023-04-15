import sys

from aiogram import executor
from loguru import logger
from pht.bot import dp
import pht.models  # noqa

import pht.routes.onboarding  # noqa
import pht.routes.menu  # noqa, must be imported by the last of routes

# remove default logger and add a nice one
logger.remove()
logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
