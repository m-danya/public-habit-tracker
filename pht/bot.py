import aiogram.types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bestconfig import Config
from pytz import utc

config = Config()
bot = Bot(token=config.BOT_TOKEN, parse_mode=aiogram.types.ParseMode.MARKDOWN_V2)
storage = RedisStorage2(
    config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PASSWORD, db=8
)
dp = Dispatcher(bot, storage=storage)


scheduler = AsyncIOScheduler(
    jobstores={
        "default": RedisJobStore(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD,
            db=7,
        )
    },
    timezone=utc,
)
