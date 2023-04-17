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
    except IntegrityError as e:
        # user is already in database, it's ok, just start onboarding as usual
        pass
    except:
        logger.exception("Couldn't create user")
        return
    await nav.send_message(Texts.onboarding_1_text, keyboard=Keyboards.onboarding_1)


@dp.message_handler(match_text(Texts.onboarding_1_next_button))
@with_navigator
async def onboarding_2(nav: Navigator):
    await nav.send_message(Texts.onboarding_2_text, keyboard=Keyboards.onboarding_2)
