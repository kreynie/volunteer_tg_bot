from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold, hcode

from src.database.exceptions import EntityAlreadyExists, EntityNotFound
from src.filters import TextFilter
from src.keyboards.inline.users import edit_users_kb, EditUsersCallback
from src.keyboards.reply.reset import reset_state_kb
from src.routers.utils import reset_user_state
from src.schemas.user import UserAddSchema, UserDeleteSchema, UserUpdatePartialSchema
from src.services.users import UsersService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.states import ManageUsersState
from src.utils.unitofwork import UnitOfWork
from .admin_keyboard import get_admin_keyboard

router = Router(name=__name__)


@router.message(ManageUsersState.addition, TextFilter(texts.done_text))
@router.message(ManageUsersState.addition_moderator_id, TextFilter(texts.done_text))
@router.message(ManageUsersState.removal, TextFilter(texts.done_text))
@router.message(ManageUsersState.editing, TextFilter(texts.done_text))
@router.message(ManageUsersState.editing_choose_field, TextFilter(texts.done_text))
@router.message(ManageUsersState.editing_chosen_field, TextFilter(texts.done_text))
async def reset_state(message: Message, state: FSMContext):
    await reset_user_state(message, state)
    await get_admin_keyboard(message)


@router.message(TextFilter(texts.add_users_text))
async def add_user(message: Message, state: FSMContext):
    await state.set_state(ManageUsersState.addition)
    await message.answer(
        "Пересылай мне сообщение нужных пользователей\n"
        "Для остановки нажми на кнопку снизу",
        reply_markup=reset_state_kb,
    )


@router.message(ManageUsersState.addition)
async def user_addition_state(message: Message, state: FSMContext):
    if message.forward_from is None or message.forward_from.is_bot is True:
        return await message.answer(
            "Не найдено пересланное сообщение пользователя\n"
            "Возможно он запретил добавлять ссылку на свою учетную "
            "запись в переадресованных сообщениях в настройках конфиденциальности"
        )

    await state.set_data(data={
        "telegram_id": message.forward_from.id,
        "username": message.forward_from.username,
    })
    await state.set_state(ManageUsersState.addition_moderator_id)
    await message.answer("Теперь пришли его MT id, нужно лишь число")


@router.message(ManageUsersState.addition_moderator_id)
async def user_addition_moderator_id(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    if message.text is None:
        return await message.answer("Мне нужен текст сообщения")
    if message.text.isdigit() is False:
        return await message.answer("Мне нужен только номер модератора в виде числа")

    user_data = await state.get_data()
    user = UserAddSchema(
        telegram_id=user_data["telegram_id"],
        moderator_id=int(message.text),
        username=user_data["username"],
    )
    try:
        await UsersService(uow).add_user(user)
    except EntityAlreadyExists:
        return await message.answer("Пользователь уже есть в базе")

    await message.answer(f"Добавлен {hbold(user.telegram_id)}")


@router.callback_query(EditUsersCallback.filter(F.action == "edit"))
async def edit_users(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        "Меню редактирования полей пользователя. "
        f"""Выбери ID пользователя для редактирования. ({hbold('поле "(1)"')})""",
        reply_markup=reset_state_kb,
    )
    await query.answer()
    await state.set_state(ManageUsersState.editing)


@router.message(ManageUsersState.editing)
async def editing_user(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer("Мне нужен текст сообщения")
    if message.text.isdigit() is False:
        return await message.answer("Мне нужен только номер модератора в виде числа")

    await state.set_data(data={
        "id": int(message.text),
    })
    await state.set_state(ManageUsersState.editing_choose_field)
    await message.answer(
        "Теперь отправь номер поля для редактирования.\n"
        f"На данный момент для редактирования доступно {hbold('только 3 поле')}"
    )


@router.message(ManageUsersState.editing_choose_field)
async def editing_user(message: Message, state: FSMContext):
    if message.text is None:
        return await message.answer("Мне нужен текст сообщения")
    if message.text.isdigit() is False:
        return await message.answer("Мне нужен только номер поля для редактирования в виде числа")

    chosen_field = int(message.text)
    if chosen_field != 3:
        return await message.answer("Выбран неверный номер поля")

    await state.update_data({
        "field_id": int(message.text)
    })
    await state.set_state(ManageUsersState.editing_chosen_field)
    await message.answer("Теперь введи необходимое значение для выбранного поля")


@router.message(ManageUsersState.editing_chosen_field)
async def editing_user_field(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    if message.text is None:
        return await message.answer("Мне нужен текст сообщения")

    choose_data = await state.get_data()
    user_edit_schema = UserUpdatePartialSchema(id=choose_data["id"])
    chosen_field_number = choose_data["field_id"]

    new_value = message.text
    match chosen_field_number:
        case 3:
            try:
                user_edit_schema.moderator_id = int(new_value)
            except ValueError:
                return await message.answer("Мне нужно целое число для редактирования ID")

    try:
        updated_user_id = await UsersService(uow).edit_user(user_edit_schema)
    except EntityNotFound:
        await message.answer("Такого человека нет в базе")
    else:
        await message.answer(f"Изменено {hbold(chosen_field_number)} поле у ID {hbold(updated_user_id)}")
    await reset_user_state(message, state)
    await get_admin_keyboard(message)


@router.message(TextFilter(texts.remove_users_text))
async def remove_user(message: Message, state: FSMContext):
    await state.set_state(ManageUsersState.removal)
    await message.answer("Перечисляй TG айди отдельными сообщениями", reply_markup=reset_state_kb)


@router.message(ManageUsersState.removal)
async def user_removal_state(message: Message, uow: UOWDep = UnitOfWork()):
    if not message.text or not message.text.isdigit():
        return await message.answer("Мне нужен айди человека. Это циферки такие, которые складываются в число")
    user_id = int(message.text)
    user = UserDeleteSchema(telegram_id=user_id)
    try:
        await UsersService(uow).delete_user(user)
    except EntityNotFound:
        return await message.answer("Такого человека нет в базе")

    await message.answer(f"Удалён {hbold(message.text)}")


@router.message(TextFilter(texts.list_users_text))
async def list_users(message: Message, uow: UOWDep = UnitOfWork()):
    users = await UsersService(uow).get_users()
    if not users:
        return await message.answer("Не найдено никого в базе")
    user_list = [
        f"(1) ID: {user.id}\n" +
        f"(2) TG ID: {hcode(user.telegram_id)}\n" +
        f"(3) МТ ID: {user.moderator_id}\n" +
        f"(4) Username: @{user.username}" if user.username else ""
        for user in users
    ]
    user_list = "\n\n".join(user_list)
    await message.answer(f"Список пользователей:\n{user_list}", reply_markup=edit_users_kb)
