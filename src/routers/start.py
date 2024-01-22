from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.keyboards.reply.main import main_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет! Для справки воспользуйся командой /info", reply_markup=main_keyboard)


@router.message(Command("menu"))
async def menu(message: Message):
    await message.answer("Меню. Для справки команда /info", reply_markup=main_keyboard)
