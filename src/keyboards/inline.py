from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from src.utils import texts


class EditRulesCallback(CallbackData, prefix="rules"):
    action: str


class ListShiftsCallback(CallbackData, prefix="shifts"):
    action: str
    page: int
    total_pages: int | None = None


edit_rules = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=texts.edit_rules_text, callback_data=EditRulesCallback(action="edit").pack()),
        ],
    ]
)


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


def edit_rules_kb(text: str, action: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=text, callback_data=EditRulesCallback(action=action).pack())
    )
    return builder.as_markup()
