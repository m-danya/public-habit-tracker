from loguru import logger

from pht.bot import dp
from pht.data import Keyboards, States, Texts
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text


@dp.message_handler(match_text(Texts.my_habits_button))
@with_navigator
async def my_habits(nav: Navigator):
    await nav.state.set_state(States.my_habits)
    await nav.send_message(Texts.my_habits_text(None), keyboard=Keyboards.my_habits)


@dp.message_handler(match_text(Texts.back_button), state=States.my_habits)
@with_navigator
async def my_habits_go_back(nav: Navigator):
    from pht.routes.menu import main_menu

    await nav.redirect(main_menu)


@dp.message_handler(state=States.my_habits)
@with_navigator
async def invalid_input_my_habits(nav: Navigator):
    await nav.send_message(Texts.invalid_input, keyboard=Keyboards.my_habits)
