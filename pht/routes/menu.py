from aiogram.types import Message

from pht.bot import bot, dp
from pht.data import Keyboards, Texts
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text


@dp.message_handler(match_text(Texts.question_button))
@with_navigator
async def answer_how(nav: Navigator):
    await nav.send_message("Пока не знаю! *Markdown test*")


@dp.message_handler(state="*")
async def _any(message: Message):
    await bot.send_message(message.chat.id, "hi", reply_markup=Keyboards.menu)
