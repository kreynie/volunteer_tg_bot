from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils import texts


class NotificationsCallback(CallbackData, prefix="notifications"):
    action: str


notifications = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=texts.enable_shifts_notifications,
                callback_data=NotificationsCallback(action="enable_shifts_notifications").pack()),
        ],
        [
            InlineKeyboardButton(
                text=texts.disable_shifts_notifications,
                callback_data=NotificationsCallback(action="disable_shifts_notifications").pack()),
        ],
    ]
)
