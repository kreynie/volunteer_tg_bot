from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils import texts


class NotificationsCallback(CallbackData, prefix="notifications"):
    action: str


notifications = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=texts.shifts_notifications,
                callback_data=NotificationsCallback(action="get_shifts_notifications").pack()),
        ],
    ]
)
