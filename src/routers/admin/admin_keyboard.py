from aiogram.types import Message

from src.keyboards.reply import admin_keyboard


async def get_admin_keyboard(message: Message):
    await message.answer("Админ панель", reply_markup=admin_keyboard)
