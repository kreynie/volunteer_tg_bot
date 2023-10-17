from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode

from src.filters import TextFilter
from src.keyboards.reply import admin_keyboard, reset_state
from src.routers.utils import reset_user_state
from src.utils.states import ManageUsersState, GetForwardedUserIDState

router = Router(name=__name__)


@router.message(Command("admin"))
async def admin_panel(message: Message):
    await get_admin_keyboard(message)


@router.message(TextFilter("взять telegram id 🆔"))
async def set_forwarded_user_id_state(message: Message, state: FSMContext):
    await state.set_state(GetForwardedUserIDState.getting)
    await message.answer("Перешли мне сообщение пользователя, ID которого нужно узнать\n"
                         "Нажми на полученное ID, чтобы скопировать", reply_markup=reset_state)


@router.message(GetForwardedUserIDState.getting, TextFilter("готово ✅"))
async def get_forwarded_user_id(message: Message, state: FSMContext):
    await reset_user_state(message, state)
    await get_admin_keyboard(message)


@router.message(GetForwardedUserIDState.getting)
async def get_forwarded_user_id(message: Message):
    if message.forward_from is None:
        await message.answer("Не найдено пересланное сообщение")
        return

    await message.answer(f"User's ID: {hcode(message.forward_from.id)}")


@router.message(TextFilter("добавить пользователя ➕"))
async def add_user(message: Message, state: FSMContext):
    await state.set_state(ManageUsersState.addition)
    await message.answer("Перечисляй айди отдельными сообщениями", reply_markup=reset_state)


@router.message(ManageUsersState.addition, TextFilter("готово ✅"))
async def add_user_state(message: Message, state: FSMContext):
    await reset_user_state(message, state)
    await get_admin_keyboard(message)


@router.message(ManageUsersState.addition)
async def add_user_state(message: Message):
    if not message.text or not message.text.isdigit():
        await message.answer("Мне нужен айди человека. Это циферки такие")
        return

    await message.answer(f"Добавлен {hbold(message.text)}")


async def get_admin_keyboard(message: Message):
    await message.answer("Админ панель", reply_markup=admin_keyboard)
