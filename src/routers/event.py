from aiogram import Router
from aiogram.types import Message

from src.filters import TextFilter
from src.schemas.shift import ShiftLogSchema, ToggleShiftSchema
from src.schemas.sort import QueryOrderBySchema
from src.schemas.user import UserGetSchema
from src.services.shifts import ShiftsService
from src.services.users import UsersService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.shift_enum import ShiftEnum
from src.utils.unitofwork import UnitOfWork

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
    shifts_limit = 6
    shift_logs = await ShiftsService(uow).get_shift_history(
        user_id=user.id,
        limit=shifts_limit,
    )
    user_shifts_text = format_shifts_history(shift_logs, number=shifts_limit)
    await message.answer(user_shifts_text)


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
        return await message.answer("Записано")
    await message.answer("Ошибка в записи")


def format_shifts_history(
        shift_logs: list[ShiftLogSchema],
        number: int,
        offset: int = 0,
        overall_amount: int = 0,
) -> str:
    if not shift_logs:
        return "Нет последних записей"
    shift_list = [
        f"ID: {shift.user_id}\n"
        f"Состояние: {shift.shift_action_name}\n"
        f"Дата/время: {shift.time:%d.%m %H:%M}"
        for shift in shift_logs
    ]
    shift_list = "\n\n".join(shift_list)
    if not offset and not overall_amount:
        return f"Последние {number} записей:\n{shift_list}"
    elif offset and not overall_amount:
        return f"Записи {offset}-{number}:\n{shift_list}"
    elif not offset and overall_amount:
        return f"Последние {number} ({overall_amount}) записей:\n{shift_list}"
    return f"Записи {offset}-{number} ({overall_amount}):\n{shift_list}"
