from aiogram.types import Update
from loguru import logger

from pht.bot import dp
from pht.data import Texts


@dp.errors_handler()
async def something_went_wrong(update: Update, error):
    await update.message.answer(Texts.something_went_wrong)
    logger.exception("Something went wrong!")
    return False
