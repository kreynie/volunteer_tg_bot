from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.utils import texts

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=texts.add_users_text),
            KeyboardButton(text=texts.remove_users_text),
            KeyboardButton(text=texts.list_users_text),
        ],
        [
            KeyboardButton(text=texts.add_rule_text),
            KeyboardButton(text=texts.remove_rule_text),
            KeyboardButton(text=texts.list_rules),
        ],
        [
            KeyboardButton(text=texts.list_shifts_text),
            KeyboardButton(text=texts.notifications),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Админка",
)
