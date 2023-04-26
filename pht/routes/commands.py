from loguru import logger
from peewee import IntegrityError

from pht.bot import dp
from pht.models import User
from pht.navigator import Navigator, with_navigator


@dp.message_handler(commands=["menu"], state="*")
@with_navigator
async def menu_command(nav: Navigator):
    from pht.routes.menu import main_menu

    await nav.redirect(main_menu)


@dp.message_handler(commands=["start"], state="*")
@with_navigator
async def start(nav: Navigator):
    await nav.state.set_state()
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
    from pht.routes.onboarding import onboarding_1

    await nav.redirect(onboarding_1)
