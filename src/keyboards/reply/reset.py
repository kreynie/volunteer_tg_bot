from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.utils import texts

reset_state_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=texts.done_text)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Нажми на кнопку, чтобы отменить",
)
