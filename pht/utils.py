from aiogram import types

from pht.bot import bot


async def send_message(user_id, text, *args, keyboard=None, **kwargs):
    """
    A wrapper for `aiogram.Bot.send_message` with extra functionality
    """

    # escape symbols that are special in Markdown
    chars_to_escape = "!<>.-()+="
    for char in chars_to_escape:
        text = text.replace(char, "\\" + char)
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
