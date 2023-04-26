from loguru import logger

from pht.bot import dp
from pht.data import Keyboards, Texts
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text


@with_navigator
async def onboarding_1(nav: Navigator):
    await nav.send_message(Texts.onboarding_1_text, keyboard=Keyboards.onboarding_1)


@dp.message_handler(match_text(Texts.onboarding_1_next_button))
@with_navigator
async def onboarding_2(nav: Navigator):
    await nav.send_message(Texts.onboarding_2_text, keyboard=Keyboards.onboarding_2)
