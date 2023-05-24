"""
This module contains functions that are used as jobs for APScheduler,
 i.e. they are called by trigger when needed (e.g. every day at specific time)

One should not use Peewee models classes as arguments for scheduler jobs, because
arguments for jobs are serialized at the moment of adding a job to scheduler and
this serialized data is stored inside Redis. In case of using Peewee model as
an argument for job, the serialized data will quickly become inconsistent with
actual User object, which will lead to data loss. Summing up, one should use
object id as an argument for a scheduler job.
"""
from collections import defaultdict
from email import message
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from contextlib import suppress

from pht.data import Texts
from pht.models import Habit, User
from pht.navigator import Navigator, with_navigator, with_navigator_for_callback
from pht.bot import dp


habit_toggle_callback = CallbackData("toggle", "habit_id")
finish_callback = CallbackData("finish")


async def ask_about_day_job(user_id):
    nav = Navigator(user_id=user_id)
    habit_values = {habit.id: 0 for habit in nav.user.habits}
    await nav.state.update_data({"habit_values": habit_values})

    await nav.send_message(Texts.ask_about_day_intro())
    await nav.send_message(**await get_asking_message_content(nav))
    # msg = "answers:"
    # for habit in user.habits:
    #     msg += str(habit.get_recent_answers)
    #     msg += "\n\n"
    # await send_message(user.id, msg)


async def get_asking_message_content(nav: Navigator):
    import random

    state = await nav.state.get_data()
    habit_values = state["habit_values"]

    buttons = [
        InlineKeyboardButton(
            text=f"{habit_values[str(habit.id)]} {habit.name}",
            callback_data=habit_toggle_callback.new(habit.id),
        )
        for habit in nav.user.habits
    ]
    buttons.append(
        InlineKeyboardButton(
            text=f"Submit",
            callback_data=finish_callback.new(),
        )
    )
    return {
        "text": f"just a message {random.randint(1, 100)}",
        "keyboard": InlineKeyboardMarkup(
            inline_keyboard=[[button] for button in buttons]
        ),
    }


@dp.callback_query_handler(habit_toggle_callback.filter())
@with_navigator_for_callback
async def habit_toggle_callback_function(nav: Navigator):
    data = await nav.state.get_data()
    habit_values = data["habit_values"]
    habit_values[nav.callback_data["habit_id"]] = not habit_values[
        nav.callback_data["habit_id"]
    ]
    await nav.state.update_data({"habit_values": habit_values})
    with suppress(MessageNotModified):
        message_content = await get_asking_message_content(nav)
        # await nav.message.edit_text(message_content["text"])
        await nav.message.edit_reply_markup(message_content["keyboard"])
