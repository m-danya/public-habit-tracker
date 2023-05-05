from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from pht.bot import bot
from pht.models import User
from pht.utils import send_message


class Navigator:
    """
    Navigator object is passed into message handlers to provide easy access to `message` and `user`
     objects and to other message-related functions.

    Navigator is attached to message handlers via `with_navigator` decorator.
    """

    def __init__(self, message: Message, state: FSMContext):
        self.message = message
        self.state = state
        self.user_id = message.from_user.id
        self.user = User.get_or_none(User.id == self.user_id)

    async def send_message(self, text, *args, keyboard=None, **kwargs):
        return await send_message(
            self.user_id, text, *args, keyboard=keyboard, **kwargs
        )

    async def redirect(self, another_route_function):
        return await another_route_function(self.message, self.state)


def with_navigator(f):
    """
    Provide Navigator object as an argument for message handler instead of `message, state`
    """

    async def wrapper(message: Message, state: FSMContext):
        nav = Navigator(message, state)
        return await f(nav)

    wrapper.__name__ = f.__name__
    return wrapper
