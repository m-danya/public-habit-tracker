from loguru import logger

from pht.bot import dp
from pht.data import Keyboards, States, Texts
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text

@dp.message_handler(match_text(Texts.settings_button))
@with_navigator
async def settings(nav: Navigator):
    await nav.state.set_state(States.settings)
    await nav.send_message(Texts.settings_text(None), keyboard=Keyboards.settings_menu)
