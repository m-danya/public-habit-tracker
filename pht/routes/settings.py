from datetime import datetime, timedelta
from loguru import logger

from pht.bot import dp
from pht.data import Keyboards, States, Texts
from pht.models import User
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text

@dp.message_handler(match_text(Texts.settings_button))
@with_navigator
async def settings(nav: Navigator):
    await nav.state.set_state(States.settings)
    await nav.send_message(Texts.settings_text(None), keyboard=Keyboards.settings_menu)

@dp.message_handler(match_text(Texts.time_setting_button), state=States.settings)
@with_navigator
async def set_time(nav: Navigator):
    await nav.state.set_state(States.settings_waiting_for_time)
    await nav.send_message(Texts.set_time_text, keyboard=Keyboards.no_buttons)

@dp.message_handler(state=States.settings_waiting_for_time)
@with_navigator
async def check_time(nav: Navigator):
    try:
        time = datetime.strptime(nav.message.text, "%H:%M").time()
    except ValueError:
        await nav.send_message(Texts.invalid_text_input)
        return

    user = User.get(User.username == nav.message.from_user.username)
    # FIXME: convert to utc+0
    user.time_to_ask = time
    user.save()

    logger.info(f"Updated time_to_ask to {time} {user}")

    await nav.redirect(settings)
