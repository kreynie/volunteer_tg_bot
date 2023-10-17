from aiogram import Router
from aiogram.types import Message
from src.filters import TextFilter

router = Router(name=__name__)


@router.message(TextFilter("зашел"))
async def take_shift(message: Message):
    await message.answer("Тут")


@router.message(TextFilter("вышел"))
async def exit_shift(message: Message):
    await message.answer("Не тут")
