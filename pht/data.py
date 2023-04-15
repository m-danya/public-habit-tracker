from pht.utils import gen_keyboard


class Texts:
    main_menu_text = "👋 Привет, ты в главном меню"
    question_button = "❓ Что делать?"
    back_button = "⬅️  Назад"
    onboarding_1_text = "Добро пожаловать! <Начало анбординга>"
    onboarding_2_text = "<Продолжение анбординга>"
    onboarding_1_next_button = "👀 Интересно"
    onboarding_2_next_button = "🤩 Я в деле"
    welcome_back = "Рад снова тебя видеть!"


class Keyboards:
    menu = gen_keyboard(
        [
            [Texts.question_button, "tbd"],
            ["tbd", "tbd"],
        ]
    )

    onboarding_1 = gen_keyboard([[Texts.onboarding_1_next_button]])
    onboarding_2 = gen_keyboard([[Texts.onboarding_2_next_button]])

    back = gen_keyboard([[Texts.back_button]])
