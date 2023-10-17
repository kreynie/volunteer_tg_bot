from aiogram import Router
from aiogram.types import Message

router = Router(name=__name__)


@router.message()
async def unknown_command(message: Message):
    await message.answer("Неизвестная команда. Воспользуйся /info для справки")
