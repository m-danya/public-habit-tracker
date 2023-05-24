import random
from pht.utils import gen_keyboard
from datetime import date, datetime, time, timedelta

from pht.utils import gen_keyboard, to_msc_time


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
        "🦾 Я создан для *отслеживания твоего прогресса по выработке привычек.*"
        "\n\n"
        "✏️ Внеси пару-тройку привычек, которых ты хочешь придерживаться, "
        "укажи периодичность, и каждый вечер я буду спрашивать "
        "тебя, удалось ли тебе преуспеть в каждой из них."
        "\n\n"
        'Например, можно добавить такие привычки: "заниматься спортом _2 раза в неделю_", '
        '"читать по 20 минут _каждый день_", '
        '"_2 раза в неделю_ гулять по часу на природе". Как видишь, можно внести почти всё что угодно.'
        "\n\n"
        "🏆 Моя фишка — **публичный рейтинг привычек**. Он подталкивает всех участников не лениться "
        "и придерживаться привычек, которые для них важны. Если хочешь, можешь не участвовать в нём, это опционально."
    )

    onboarding_2_text = "<Продолжение анбординга>"
    onboarding_1_next_button = "👀 Интересно"
    onboarding_2_next_button = "🤩 Я в деле"
    invalid_buttons_input = (
        "Здесь нужно нажать на одну из кнопок 🤔\n\n"
        "Если бот заблудился, нажми /menu и сообщи о произошедшем @m\\_danya\\_jpg"
    )
    invalid_text_input = (
        "Что-то ты не то пишешь, попробуй ещё раз 🤔\n\n"
        "Если бот заблудился, нажми /menu и сообщи о произошедшем @m\\_danya\\_jpg"
    )
    something_went_wrong = (
        "Что\\-то пошло не так\!\n\nПожалуйста, напиши об этом @m\\_danya\\_jpg"
    )

    time_setting_button = "🕒 Время опроса"
    rating_setting_button = "🏆 Участие в рейтинге"

    set_time_text = "⏳ Введи время в часовом поясе UTC+3:00 (по Москве) в формате HH:MM"
    set_rating_text = "🏅 Ты будешь участвовать в публичном рейтинге?"

    @staticmethod
    def my_habits_text(habits: ...):
        header = "*Твои привычки:*"
        habits = [
            "- *Заниматься спортом*: два раза в неделю",
            "- *Не есть сладкое после ужина*: каждый день",
        ]
        return header + "\n\n" + "\n".join(habits)

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
        header = "*Твои настройки:*"

        time_str = f"{time.strftime(to_msc_time(time_to_ask), '%H:%M')}"
        rating_str = "да" if rating_publicity else "нет"

        settings = [
            f"- *Время опроса*: {time_str} (UTC+3:00)",
            f"- *Участие в публичном рейтинге*: {rating_str}",
        ]
        return header + "\n\n" + "\n".join(settings)

    @staticmethod
    def ask_about_day_intro(*args, **kwargs):
        return f"""{random.choice(Texts.greeting)} Посмотрим на твой прогресс:

        <список привычек с эмодзи по дням недели>
        """

    @staticmethod
    def ask_about_day_main(*args, **kwargs):
        return f"""Давай внесём результаты за сегодня:"""

    add_new_habit_intro_text = (
        "Отлично! Я спрошу тебя о нескольких вещах:\n\n"
        "- Название привычки (_читать по 10 минут_)\n"
        "- Периодичность (_каждый день_)\n"
        "- Тип ответа (_количество минут в день_)\n\n"
        "Но, обо всём по порядку!"
    )

    add_new_habit_name_text = "1⃣️ Отправь мне *название привычки*:"
    add_new_habit_regularity_text = (
        "2⃣ *Сколько раз в неделю* ты хочешь выполнять эту привычку?\n\n"
        "Я не спрашиваю, в какие дни недели ты хочешь придерживаться привычки, "
        "так как жизнь — штука нестабильная, наверняка хоть раз что-то куда-то съедет.\n\n"
        "Поэтому просто будем ориентироваться на количество дней в неделю, так удобнее 👌🏻"
    )
    add_new_habit_choose_type_text = (
        "3⃣ Как будешь отслеживать прогресс?\n\n"
        "Могу просто спрашивать, *удалось ли* придерживаться привычки, а могу "
        "спрашивать *количество минут*, которые получилось уделить привычке."
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
