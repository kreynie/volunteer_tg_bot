from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зашел 🟢"),
            KeyboardButton(text="Вышел 🔴"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие",
)

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить пользователя ➕"),
            KeyboardButton(text="Убрать пользователя ❌"),
            KeyboardButton(text="Список 📃"),
        ],
        [
            KeyboardButton(text="Взять Telegram ID 🆔"),
            KeyboardButton(text="Посмотреть логи 📅"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Админка",
)

reset_state = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Готово ✅")]
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
