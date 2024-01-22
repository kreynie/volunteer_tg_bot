from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils import texts


class EditUsersCallback(CallbackData, prefix="users"):
    action: str


edit_users_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=texts.edit_users_text, callback_data=EditUsersCallback(action="edit").pack()),
        ],
    ]
)


def get_edit_users_kb(text: str, action: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=text, callback_data=EditUsersCallback(action=action).pack())
    )
    return builder.as_markup()
