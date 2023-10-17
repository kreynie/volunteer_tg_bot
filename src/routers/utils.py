from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router(name=__name__)


async def reset_user_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Завершено")
