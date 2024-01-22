from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils import texts


class EditRulesCallback(CallbackData, prefix="rules"):
    action: str


edit_rules = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=texts.edit_rules_text, callback_data=EditRulesCallback(action="edit").pack()),
        ],
    ]
)


def edit_rules_kb(text: str, action: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=text, callback_data=EditRulesCallback(action=action).pack())
    )
    return builder.as_markup()
