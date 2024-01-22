from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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
