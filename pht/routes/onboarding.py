from loguru import logger
from peewee import IntegrityError

from pht.bot import dp
from pht.data import Keyboards, Texts
from pht.models import User
from pht.navigator import Navigator, with_navigator
from pht.utils import match_text


@dp.message_handler(commands=["start"])
@with_navigator
async def start(nav: Navigator):
    try:
        user = User.create(
            id=nav.message.from_id,
            username=nav.message.from_user.username,
            full_name=nav.message.from_user.full_name,
        )
        logger.info(f"New user {user}")
        await nav.send_message(Texts.onboarding_1_text, keyboard=Keyboards.onboarding_1)
    except IntegrityError as e:
        await nav.send_message(Texts.welcome_back)
    except:
        logger.exception("Couldn't create user")


@dp.message_handler(match_text(Texts.onboarding_1_next_button))
@with_navigator
async def onboarding_2(nav: Navigator):
    await nav.send_message(Texts.onboarding_2_text, keyboard=Keyboards.onboarding_2)
