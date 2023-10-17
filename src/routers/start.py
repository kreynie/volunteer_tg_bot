from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards.reply import main_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет! Для справки воспользуйся командой /info", reply_markup=main_keyboard)
