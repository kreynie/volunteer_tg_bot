from aiogram import Router
from aiogram.types import Message
from src.filters import TextFilter
from src.schemas.shift import ToggleShiftSchema
from src.schemas.user import UserGetSchema
from src.services.shifts import ShiftsService
from src.services.users import UsersService
from src.utils.dependencies import UOWDep
from src.utils.shift_enum import ShiftEnum
from src.utils.unitofwork import UnitOfWork
from src.utils import texts

router = Router(name=__name__)


@router.message(TextFilter(texts.enter_shift))
async def take_shift(message: Message):
    await toggle_shift(message=message, shift_enum=ShiftEnum.enter)


@router.message(TextFilter(texts.exit_shift))
async def exit_shift(message: Message):
    await toggle_shift(message=message, shift_enum=ShiftEnum.exit)


@router.message(TextFilter(texts.my_shifts))
async def get_user_shifts(message: Message, uow: UOWDep = UnitOfWork()):
    user_data = UserGetSchema(telegram_id=message.from_user.id)
    user = await UsersService(uow).get_user(user_data)
    users_shifts = await get_shifts_history(user.id)
    await message.answer(users_shifts)


async def toggle_shift(message: Message, shift_enum: ShiftEnum, uow: UOWDep = UnitOfWork()):
    user = UserGetSchema(telegram_id=message.from_user.id)
    user = await UsersService(uow).get_user(user)
    shift = ToggleShiftSchema(
        user_id=user.id,
        shift_action_id=shift_enum.value,
        time=message.date,
    )
    shift_id = await ShiftsService(uow).toggle_shift(shift)
    if shift_id:
        await message.answer("Записано")
        return
    await message.answer("Ошибка в записи")


async def get_shifts_history(
        user_id: int | None = None,
        limit: int = 10,
        uow: UOWDep = UnitOfWork()
) -> str:
    shift_logs = await ShiftsService(uow).get_shift_history(user_id, limit)
    if not shift_logs:
        return "Нет последних записей"
    shift_list = [
        (f"ID: {shift.user_id}\n" if user_id is None else "") +
        (f"Состояние: {ShiftEnum(shift.shift_action_id).name}\n"
         f"Дата/время: {shift.time:%d.%m %H:%M}")
        for shift in shift_logs
    ]
    shift_list = "\n\n".join(shift_list)
    return f"Последние {limit} записей:\n{shift_list}"
