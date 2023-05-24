from typing import Optional
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from pht.bot import bot, dp
from pht.models import User
from pht.utils import send_message


class Navigator:
    """
    Navigator object is passed into message handlers to provide easy access to `message` and `user`
     objects and to other message-related functions.

    Navigator is attached to message handlers via `with_navigator` decorator.
    """

    def __init__(
        self,
        message: Optional[Message] = None,
        state: Optional[FSMContext] = None,
        call: Optional[CallbackQuery] = None,
        callback_data: Optional[dict] = None,
        user_id: Optional[int] = None,
    ):
        if message:
            self.message = message
            self.state = state
            self.user_id = message.from_user.id
        elif call:
            self.call = call
            self.message = self.call.message
            self.user_id = self.message.chat.id
            self.state = state
            self.callback_data = callback_data
        else:
            self.user_id: int | None = user_id
            self.state = dp.current_state(user=self.user_id)

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
        nav = Navigator(message=message, state=state)
        return await f(nav)

    wrapper.__name__ = f.__name__
    return wrapper


def with_navigator_for_callback(f):
    """
    Provide Navigator object as an argument for callback instead of `call`
    """

    async def wrapper(call: CallbackQuery, state: FSMContext, callback_data: dict):
        nav = Navigator(call=call, state=state, callback_data=callback_data)
        return await f(nav)

    wrapper.__name__ = f.__name__
    return wrapper
