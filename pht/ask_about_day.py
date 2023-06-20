"""
This module is about asking user about his/her day.

It contains `ask_about_day_job` function that is used as job for APScheduler,
 i.e. it is called by trigger when needed (e.g. every day at specific time)

One should not use Peewee models classes as arguments for scheduler jobs, because
arguments for jobs are serialized at the moment of adding a job to scheduler and
this serialized data is stored inside Redis. In case of using Peewee model as
an argument for job, the serialized data will quickly become inconsistent with
actual User object, which will lead to data loss. Summing up, one should use
object id as an argument for a scheduler job.
"""
from collections import defaultdict
from datetime import date
from email import message
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from contextlib import suppress

from pht.data import IntegerInputRequired, Keyboards, States, Texts
from pht.models import Answer, Habit, User
from pht.navigator import Navigator, with_navigator, with_navigator_for_callback
from pht.bot import dp
from pht.utils import today


habit_toggle_callback = CallbackData("toggle", "habit_id", "day")
finish_callback = CallbackData("finish")


async def ask_about_day_job(user_id):
    nav = Navigator(user_id=user_id)
    await ask_about_day(nav, today())


async def ask_about_day(nav: Navigator, day: date):
    await nav.state.set_state(States.ask_about_day_main)
    await nav.send_message(
        Texts.ask_about_day_intro(nav.user.habits), reply_markup=Keyboards.no_buttons
    )
    await nav.send_message(**await get_asking_message_content(nav, day))


async def get_asking_message_content(nav: Navigator, day: date):
    buttons = []
    for habit in nav.user.habits:
        habit_status = habit.get_status_for_day(day)
        if not habit_status.emoji:
            # There was no such habit at that day
            continue
        button_text = f"{habit_status.emoji} {habit.name}"
        if habit.answer_type == "integer" and habit_status.value:
            button_text += f" ({habit_status.value} мин)"
        buttons.append(
            InlineKeyboardButton(
                text=button_text,
                # CallbackData does not support datetime.date => store `day`
                # as a number of days since 01.01.01 (`.toordinal()`)
                callback_data=habit_toggle_callback.new(habit.id, day.toordinal()),
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=Texts.submit_button,
            callback_data=finish_callback.new(),
        )
    )
    return {
        "text": Texts.ask_about_day_main(day),
        "keyboard": InlineKeyboardMarkup(
            inline_keyboard=[[button] for button in buttons]
        ),
    }


@dp.callback_query_handler(
    habit_toggle_callback.filter(), state=States.ask_about_day_main
)
@with_navigator_for_callback
async def habit_toggle_callback_function(nav: Navigator):
    habit = Habit.get_by_id(nav.callback_data["habit_id"])
    day = date.fromordinal(int(nav.callback_data["day"]))
    try:
        Answer.toggle(habit, day)
    except IntegerInputRequired:
        with suppress(MessageNotModified):
            await nav.message.edit_text(Texts.ask_about_day_integer_input_text(habit))
            await nav.message.edit_reply_markup(None)
        await nav.state.set_data({"habit_id": habit.id, "day": day.toordinal()})
        await nav.state.set_state(States.ask_about_day_integer_input)
        await nav.call.answer()
        return

    with suppress(MessageNotModified):
        message_content = await get_asking_message_content(nav, day)
        # do not call `nav.message.edit_text` here to avoid message shaking
        await nav.message.edit_reply_markup(message_content["keyboard"])
    await nav.call.answer()


@dp.callback_query_handler(finish_callback.filter(), state=States.ask_about_day_main)
@with_navigator_for_callback
async def finish_callback_function(nav: Navigator):
    with suppress(MessageNotModified):
        await nav.message.edit_text(Texts.day_submitted)
        await nav.message.edit_reply_markup()
    await nav.call.answer()
    from pht.routes.menu import main_menu_nav

    await main_menu_nav(nav)


@dp.message_handler(state=States.ask_about_day_integer_input)
@with_navigator
async def integer_input_function(nav: Navigator):
    data = await nav.state.get_data()
    habit = Habit.get_by_id(data["habit_id"])
    day = date.fromordinal(int(data["day"]))
    try:
        value = int(nav.message.text)
        if value < 0:
            raise ValueError
        Answer.set_integer_value(habit, day, value)
    except ValueError:
        await nav.send_message(Texts.invalid_any_value)
        return
    await nav.state.set_state(States.ask_about_day_main)
    await nav.send_message(**await get_asking_message_content(nav, day))
