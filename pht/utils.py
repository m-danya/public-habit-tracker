from aiogram import types


def gen_keyboard(keyboard):
    if not keyboard:
        return types.ReplyKeyboardRemove()
    return types.ReplyKeyboardMarkup(
        [[types.KeyboardButton(btn) for btn in row] for row in keyboard],
        resize_keyboard=True,
    )


def match_text(text):
    return lambda m: m.text == text
