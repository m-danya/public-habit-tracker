from aiogram.types import Message

from pht.bot import bot, dp
from pht.data import Keyboards, Texts
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text


@dp.message_handler(match_text(Texts.question_button))
@with_navigator
async def what_to_do(nav: Navigator):
    from pht.routes.onboarding import start

    await nav.redirect(start)


@dp.message_handler(state="*")
@with_navigator
async def main_menu(nav: Navigator):
    await main_menu_nav(nav)


async def main_menu_nav(nav: Navigator):
    # this function is necessary for callbacks, as they don't have `message`
    # and `Navigator.redirect` doesn't work because Navigator's reconstruction fails
    await nav.state.set_state()
    await nav.send_message(Texts.main_menu_text, reply_markup=Keyboards.menu)
