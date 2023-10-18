from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.utils import texts

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=texts.enter_shift),
            KeyboardButton(text=texts.exit_shift),
        ],
        [
            KeyboardButton(text=texts.my_shifts),
        ],
        [
            KeyboardButton(text=texts.list_rules)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие",
)

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=texts.add_users_text),
            KeyboardButton(text=texts.remove_users_text),
            KeyboardButton(text=texts.list_users_text),
        ],
        [
            KeyboardButton(text=texts.add_rule_text),
            KeyboardButton(text=texts.list_rules),
        ],
        [
            KeyboardButton(text=texts.list_shifts_text),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Админка",
)

reset_state = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts.done_text)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Нажми на кнопку, чтобы прекратить",
)


def keyboard_gen(
        text: str | list[str],
        one_time_keyboard: bool = False,
        **kwargs,
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=button) for button in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard, **kwargs)
