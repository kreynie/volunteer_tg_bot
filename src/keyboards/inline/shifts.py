from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils import texts


class ListShiftsCallback(CallbackData, prefix="shifts"):
    action: str
    page: int
    total_pages: int | None = None


def shifts_list_paginator(page: int, total_pages: int):
    builder = InlineKeyboardBuilder()
    buttons = []
    if page > 0:
        buttons.append(
            InlineKeyboardButton(
                text=texts.previous_page,
                callback_data=ListShiftsCallback(action=texts.previous_page_action, page=page).pack(),
            ),
        )

    if page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text=texts.next_page,
                callback_data=ListShiftsCallback(
                    action=texts.next_page_action,
                    page=page,
                    total_pages=total_pages,
                ).pack(),
            ),
        )
    builder.row(*buttons, width=2)
    return builder.as_markup()
