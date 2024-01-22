from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode

from src.database.exceptions import EntityAlreadyExists, EntityNotFound
from src.filters import TextFilter
from src.keyboards.reply.reset import reset_state
from src.routers.utils import reset_user_state
from src.schemas.user import UserAddSchema, UserDeleteSchema
from src.services.users import UsersService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.states import ManageUsersState
from src.utils.unitofwork import UnitOfWork
from .admin_keyboard import get_admin_keyboard

router = Router(name=__name__)


@router.message(ManageUsersState.addition, TextFilter(texts.done_text))
@router.message(ManageUsersState.removal, TextFilter(texts.done_text))
async def reset_removal_user_state(message: Message, state: FSMContext):
    await reset_user_state(message, state)
    await get_admin_keyboard(message)


@router.message(TextFilter(texts.add_users_text))
async def add_user(message: Message, state: FSMContext):
    await state.set_state(ManageUsersState.addition)
    await message.answer("Пересылай мне сообщение нужных пользователей\n"
                         "Для остановки нажми на кнопку снизу", reply_markup=reset_state)


@router.message(ManageUsersState.addition)
async def user_addition_state(message: Message, uow: UOWDep = UnitOfWork()):
    if message.forward_from is None or message.forward_from.is_bot is True:
        return await message.answer("Не найдено пересланное сообщение пользователя\n"
                                    "Возможно он запретил добавлять ссылку на свою учетную "
                                    "запись в переадресованных сообщениях в настройках конфиденциальности")
    user = UserAddSchema(
        telegram_id=message.forward_from.id,
        username=message.forward_from.username,
    )
    try:
        await UsersService(uow).add_user(user)
    except EntityAlreadyExists:
        return await message.answer("Пользователь уже есть в базе")

    await message.answer(f"Добавлен {hbold(user.telegram_id)}")


@router.message(TextFilter(texts.remove_users_text))
async def remove_user(message: Message, state: FSMContext):
    await state.set_state(ManageUsersState.removal)
    await message.answer("Перечисляй TG айди отдельными сообщениями", reply_markup=reset_state)


@router.message(ManageUsersState.removal)
async def user_removal_state(message: Message, uow: UOWDep = UnitOfWork()):
    if not message.text or not message.text.isdigit():
        return await message.answer("Мне нужен айди человека. Это циферки такие")
    user_id = int(message.text)
    user = UserDeleteSchema(telegram_id=user_id)
    try:
        await UsersService(uow).delete_user(user)
    except EntityNotFound:
        return await message.answer("Пользователя нет в базе")

    await message.answer(f"Удалён {hbold(message.text)}")


@router.message(TextFilter(texts.list_users_text))
async def list_users(message: Message, uow: UOWDep = UnitOfWork()):
    users = await UsersService(uow).get_users()
    if not users:
        return await message.answer("Не найдено никого в базе")
    user_list = [
        (f"ID: {user.id}\n"
         f"TG ID: {hcode(user.telegram_id)}") +
        (f"\nUsername: @{user.username}" if user.username else "")
        for user in users
    ]
    user_list = "\n\n".join(user_list)
    await message.answer(f"Список пользователей:\n{user_list}")
