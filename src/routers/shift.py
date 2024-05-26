from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from sqlalchemy.exc import DatabaseError

from src.filters import TextFilter
from src.schemas.notifications import GetUsersWithNotificationSchema
from src.schemas.shift import ShiftLogSchema, ToggleShiftSchema
from src.schemas.user import UserGetSchema
from src.services.notifications import NotificationsService
from src.services.shifts import ShiftsService
from src.services.users import UsersService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.notifications_enum import NotificationsEnum
from src.utils.shift_enum import ShiftEnum
from src.utils.unitofwork import UnitOfWork
from src.utils.pluralization import plural_form

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

    displayed_shifts_number = min(shifts_limit, len(shift_logs))
    user_shifts_text = format_shifts_history(
        shift_logs=shift_logs,
        number=displayed_shifts_number,
    )
    await message.answer(user_shifts_text)


async def toggle_shift(message: Message, shift_enum: ShiftEnum, uow: UOWDep = UnitOfWork()):
    user = UserGetSchema(telegram_id=message.from_user.id)
    user = await UsersService(uow).get_user(user)

    # Due to TG sometimes gives wrong local time, message.date replaced with datetime.now()
    shift = ToggleShiftSchema(
        user_id=user.id,
        shift_action_id=shift_enum.value,
        time=datetime.now(),
    )
    try:
        await ShiftsService(uow).toggle_shift(shift)
    except DatabaseError:
        return await message.answer("Произошла ошибка во время добавления записи в БД")
    except Exception as e:
        return await message.answer("Произошла непредвиденная ошибка при попытке записи\n"
                                    f"<code>{e}</code>")

    action_emoji = "🟢" if shift_enum == ShiftEnum.enter else "🔴"
    await message.answer(f"Записано {action_emoji}")

    action_message = "зашел на смену" if shift_enum == ShiftEnum.enter else "вышел со смены"
    get_users_to_notify = await NotificationsService(uow).get_users_with_notification(
        GetUsersWithNotificationSchema(notification_id=NotificationsEnum.shifts.value, enabled=True)
    )
    for user_to_notify in get_users_to_notify:
        if user_to_notify.user_id == user.telegram_id:
            continue

        await message.bot.send_message(
            chat_id=user_to_notify.user_id,
            text=f'<a href="tg://user?id={user.telegram_id}">Модератор</a> {user.moderator_id} {action_message}'
        )


def format_shifts_history(
        shift_logs: list[ShiftLogSchema],
        number: int,
        offset: int = 0,
        overall_amount: int = 0,
) -> str:
    if not shift_logs:
        return "Нет последних записей"
    shift_list = [
        f"MT ID: {shift.moderator_id}\n"
        f"Состояние: {shift.shift_action_name}\n"
        f"Дата/время: {shift.time:%d.%m %H:%M}"
        for shift in shift_logs
    ]
    shift_list = "\n\n".join(shift_list)
    records_word = plural_form(number, "запись", "записи", "записей")
    if not offset and not overall_amount:
        return f"Последние {number} {records_word}:\n{shift_list}"
    elif offset and not overall_amount:
        return f"Последние {offset}-{offset + number - 1} {records_word}:\n{shift_list}"
    elif not offset and overall_amount:
        return f"Последние {number} ({overall_amount}) {records_word}:\n{shift_list}"
    return f"Записи {offset}-{offset + number - 1} ({overall_amount}):\n{shift_list}"
