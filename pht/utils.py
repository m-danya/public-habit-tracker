from aiogram import types
from datetime import date, datetime, time, timedelta

from pht.bot import bot


async def send_message(user_id, text, *args, keyboard=None, **kwargs):
    """
    A wrapper for `aiogram.Bot.send_message` with extra functionality
    """

    if keyboard:
        kwargs["reply_markup"] = keyboard
    return await bot.send_message(user_id, text, *args, **kwargs)


def gen_keyboard(keyboard):
    if not keyboard:
        return types.ReplyKeyboardRemove()
    return types.ReplyKeyboardMarkup(
        [[types.KeyboardButton(btn) for btn in row] for row in keyboard],
        resize_keyboard=True,
    )


def match_text(text):
    return lambda m: m.text == text


def to_utc_time(time_msc):
    return (datetime.combine(date.today(), time_msc) - timedelta(hours=3)).time()


def to_msc_time(time_utc):
    return (datetime.combine(date.today(), time_utc) + timedelta(hours=3)).time()
