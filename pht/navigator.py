from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from pht.bot import bot


class Navigator:
    def __init__(self, message: Message, state: FSMContext):
        self.message = message
        self.state = state
        self.user_id = message.from_user.id

    async def send_message(self, text, *args, keyboard=None, **kwargs):
        chars_to_escape = "!<>"
        for char in chars_to_escape:
            text = text.replace(char, "\\" + char)
        if keyboard:
            kwargs["reply_markup"] = keyboard
        return await bot.send_message(self.user_id, text, *args, **kwargs)


def with_navigator(f):
    async def wrapper(message: Message, state: FSMContext):
        nav = Navigator(message, state)
        return await f(nav)

    wrapper.__name__ = f.__name__
    return wrapper
