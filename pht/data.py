import random
from datetime import date, datetime, time, timedelta

from pht.utils import (
    days_left_till_sunday,
    gen_keyboard,
    get_nearest_monday,
    to_msc_time,
    today,
)


SCHEDULER_FORGET_IF_MISSED_SECONDS = 60 * 120


class Texts:
    main_menu_text = "👋 Ты в главном меню"
    my_habits_button = "🦾 Мои привычки"
    add_habit_button = "➕ Добавить привычку"
    rating_button = "🏆 Рейтинг"
    change_past_button = "⏪ Изменить прошлое"
    settings_button = "⚙️ Настройки"
    question_button = "❓ Что делать?"
    back_button = "⬅️  Назад"
    onboarding_1_text = (
        "🦾 Я создан для <b>отслеживания твоего прогресса по выработке привычек.</b>"
        "\n\n"
        "✏️ Внеси пару-тройку привычек, которых ты хочешь придерживаться, "
        "укажи периодичность, и каждый вечер я буду спрашивать "
        "тебя, удалось ли тебе преуспеть в каждой из них."
        "\n\n"
        'Например, можно добавить такие привычки: "заниматься спортом <i>2 раза в неделю</i>", '
        '"читать по 20 минут <i>каждый день</i>", '
        '"<i>2 раза в неделю</i> гулять по часу на природе". Как видишь, можно внести почти всё что угодно.'
        "\n\n"
        "🏆 Моя фишка — <b>публичный рейтинг привычек</b>. Он подталкивает всех участников не лениться "
        "и придерживаться привычек, которые для них важны. Если хочешь, можешь не участвовать в нём, это опционально."
    )

    onboarding_2_text = "Здесь будет продолжение анбординга"
    onboarding_1_next_button = "👀 Интересно"
    onboarding_2_next_button = "🤩 Я в деле"
    invalid_buttons_input = (
        "Здесь нужно нажать на одну из кнопок 🤔\n\n"
        "Если бот заблудился, нажми /menu и сообщи о произошедшем @m_danya_jpg"
    )
    invalid_text_input = (
        "Что-то ты не то пишешь, попробуй ещё раз 🤔\n\n"
        "Если бот заблудился, нажми /menu и сообщи о произошедшем @m_danya_jpg"
    )
    something_went_wrong = (
        "Что-то пошло не так!\n\nПожалуйста, напиши об этом @m_danya_jpg"
    )

    change_past_text = (
        "Здесь ты можешь внести информацию о прошлом дне, если понял, что внёс что-то не так.\n\n"
        'За какой день ты хочешь изменить информацию о привычках? Пришли ответ в формате "дд.мм.гггг", '
        'например, "31.12.2022"'
    )

    time_setting_button = "🕒 Время опроса"
    rating_setting_button = "🏆 Участие в рейтинге"

    set_time_text = "⏳ Введи время в часовом поясе UTC+3:00 (по Москве) в формате HH:MM"
    set_rating_text = "🏅 Ты будешь участвовать в публичном рейтинге?"

    @staticmethod
    def my_habits_text(habits):
        header = "<b>Твои привычки:</b>"
        habit_texts = [
            f"- {habit.type_emoji} <b>{habit.name}</b>: {Texts.regularity_to_text[habit.regularity]}"
            for habit in habits
        ]
        return header + "\n\n" + "\n".join(habit_texts)

    @staticmethod
    def habits_with_emojis(habits):
        def _get_emojis(habit):
            from_date = get_nearest_monday(today())
            n_days = 7 - days_left_till_sunday(today())
            return "".join(
                habit.get_status_for_day(
                    from_date + timedelta(days=day_n), empty_emoji="⏸️"
                ).emoji
                for day_n in range(n_days)
            )

        return "\n".join(
            [
                f"- {habit.type_emoji} <b>{habit.name}</b>:\n\n{_get_emojis(habit)}\n"
                for habit in habits
            ]
        )

    greeting = [
        "Привет, как дела?",
        "Привет, как успехи?",
        "Привет!",
        "Здравствуй!",
        "Здравствуй! Как дела?",
        "Привет!",
    ]

    @staticmethod
    def settings_text(time_to_ask, rating_publicity):
        header = "<b>Твои настройки:</b>"

        time_str = f"{time.strftime(to_msc_time(time_to_ask), '%H:%M')}"
        rating_str = "да" if rating_publicity else "нет"

        settings = [
            f"- <b>Время опроса</b>: {time_str} (UTC+3:00)",
            f"- <b>Участие в публичном рейтинге</b>: {rating_str}",
        ]
        return header + "\n\n" + "\n".join(settings)

    @staticmethod
    def ask_about_day_intro(habits):
        return f"{random.choice(Texts.greeting)} Посмотрим на твой прогресс на этой неделе:\n\n{Texts.habits_with_emojis(habits)}"

    @staticmethod
    def ask_about_day_main(day: date):
        return f"Давай внесём результаты за {Texts.date_to_text(day)}:"

    @staticmethod
    def ask_about_day_integer_input_text(habit):
        return f"<b>{habit.name}</b>\n\nСколько минут удалось уделить этой привычке?"

    # it is used in at least 2 places, be careful when changing
    invalid_any_value = "Некорректное значение, попробуй ещё раз"

    submit_button = "Сохранить"
    day_submitted = "Принято!"

    regularity_to_text = {
        1: "1 раз в неделю",
        2: "2 раза в неделю",
        3: "3 раза в неделю",
        4: "4 раза в неделю",
        5: "5 раз в неделю",
        6: "6 раз в неделю",
        7: "каждый день",
    }

    def date_to_text(day: date):
        if day == today():
            return "сегодня"
        else:
            return day.strftime("%d.%m")

    add_new_habit_intro_text = (
        "Отлично! Я спрошу тебя о нескольких вещах:\n\n"
        "- Название привычки (<i>читать по 10 минут</i>)\n"
        "- Периодичность (<i>каждый день</i>)\n"
        "- Тип ответа (<i>количество минут в день</i>)\n\n"
        "Но, обо всём по порядку!"
    )

    add_new_habit_name_text = "1⃣️ Отправь мне <b>название привычки</b>:"
    add_new_habit_regularity_text = (
        "2⃣ <b>Сколько раз в неделю</b> ты хочешь выполнять эту привычку?\n\n"
        "Я не спрашиваю, в какие дни недели ты хочешь придерживаться привычки, "
        "так как жизнь — штука нестабильная, наверняка хоть раз что-то куда-то съедет.\n\n"
        "Поэтому просто будем ориентироваться на количество дней в неделю, так удобнее 👌🏻"
    )
    add_new_habit_choose_type_text = (
        "3⃣ Как будешь отслеживать прогресс?\n\n"
        "Могу просто спрашивать, <b>удалось ли</b> придерживаться привычки, а могу "
        "спрашивать <b>количество минут</b>, которые получилось уделить привычке."
    )
    add_new_habit_button_yes_no = "🚩 да/нет"
    add_new_habit_button_minutes = "⏰ количество минут в день"
    add_new_habit_success = "🎉 Привычка добавлена!"

    yes_button = "👍 Да"
    no_button = "👎 Нет"


class Keyboards:
    menu = gen_keyboard(
        [
            [Texts.my_habits_button, Texts.rating_button],
            [Texts.question_button, Texts.settings_button],
        ]
    )

    onboarding_1 = gen_keyboard([[Texts.onboarding_1_next_button]])
    onboarding_2 = gen_keyboard([[Texts.onboarding_2_next_button]])

    my_habits = gen_keyboard(
        [[Texts.add_habit_button], [Texts.change_past_button], [Texts.back_button]]
    )

    back = gen_keyboard([[Texts.back_button]])

    add_new_habit_regularity = gen_keyboard([["1", "2", "3", "4", "5", "6", "7"]])
    add_new_habit_type = gen_keyboard(
        [[Texts.add_new_habit_button_yes_no], [Texts.add_new_habit_button_minutes]]
    )

    no_buttons = gen_keyboard(None)

    settings_menu = gen_keyboard(
        [[Texts.time_setting_button, Texts.rating_setting_button], [Texts.back_button]]
    )

    yes_no_menu = gen_keyboard([[Texts.yes_button, Texts.no_button]])


class States:
    my_habits = "my_habits"
    add_new_habit_intro = "add_new_habit_intro"
    add_new_habit_waiting_for_name = "add_new_habit_waiting_for_name"
    add_new_habit_waiting_for_regularity = "add_new_habit_waiting_for_regularity"
    add_new_habit_waiting_for_type = "add_new_habit_waiting_for_type"

    settings = "settings"
    settings_waiting_for_time = "settings_waiting_for_time"
    settings_waiting_for_rating = "settings_waiting_for_rating"

    ask_about_day_main = "ask_about_day_main"
    ask_about_day_integer_input = "ask_about_day_integer_input"

    change_past_waiting_for_date = "change_past_waiting_for_date"


class IntegerInputRequired(Exception):
    """
    Exception for toggle_callback

    It is raised when user toggles a habit with integer value from zero-value to
    non-zero. At this situation, an integer value is required from user.

    This exception is not an error, it just helps to handle the situation more
    easily that a bunch of "if"s.
    """

    pass
