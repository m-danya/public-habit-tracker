from loguru import logger

from pht.bot import dp
from pht.data import Keyboards, States, Texts
from pht.models import Habit
from pht.navigator import Navigator, with_navigator


@with_navigator
async def add_new_habit_intro_and_ask_for_name(nav: Navigator):
    await nav.state.set_state(States.add_new_habit_waiting_for_name)
    await nav.send_message(
        Texts.add_new_habit_intro_text, keyboard=Keyboards.no_buttons
    )
    await nav.send_message(Texts.add_new_habit_name_text)


@dp.message_handler(state=States.add_new_habit_waiting_for_name)
@with_navigator
async def add_new_habit_check_name(nav: Navigator):
    await nav.state.update_data({"name": nav.message.text})
    await nav.state.set_state(States.add_new_habit_waiting_for_regularity)
    await nav.send_message(
        Texts.add_new_habit_regularity_text, keyboard=Keyboards.add_new_habit_regularity
    )


@dp.message_handler(state=States.add_new_habit_waiting_for_regularity)
@with_navigator
async def add_new_habit_check_regularity(nav: Navigator):
    regularity = nav.message.text
    try:
        regularity = int(regularity)
        if regularity not in range(1, 7 + 1):
            raise ValueError
    except ValueError:
        await nav.send_message(Texts.invalid_text_input)
        return
    await nav.state.set_state(States.add_new_habit_waiting_for_type)
    await nav.state.update_data({"regularity": int(regularity)})
    await nav.send_message(
        Texts.add_new_habit_choose_type_text, keyboard=Keyboards.add_new_habit_type
    )


@dp.message_handler(state=States.add_new_habit_waiting_for_type)
@with_navigator
async def add_new_habit_check_type_and_finish(nav: Navigator):
    answer_type_input = nav.message.text
    match answer_type_input:
        case Texts.add_new_habit_button_yes_no:
            answer_type = "yes or no"
        case Texts.add_new_habit_button_minutes:
            answer_type = "minutes"
        case _:
            await nav.send_message(Texts.invalid_text_input)
            return

    await nav.state.update_data({"answer_type": answer_type})
    state = await nav.state.get_data()
    habit = Habit.create(
        owner=nav.user,
        name=state["name"],
        answer_type=state["answer_type"],
        regularity=state["regularity"],
    )
    logger.info(f"New habit {habit}")

    from pht.routes.menu import main_menu

    await nav.send_message(Texts.add_new_habit_success)
    await nav.redirect(main_menu)
