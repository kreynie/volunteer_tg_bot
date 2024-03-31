from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.filters import TextFilter
from src.keyboards.inline.notifications import notifications as notifications_kb, NotificationsCallback
from src.schemas import notifications as schemas
from src.services.notifications import NotificationsService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.notifications_enum import NotificationsEnum
from src.utils.unitofwork import UnitOfWork

router = Router(name=__name__)


@router.message(TextFilter(texts.notifications))
async def take_shift(message: Message):
    await message.answer("Параметры уведомлений о посещалке", reply_markup=notifications_kb)


@router.callback_query(NotificationsCallback.filter(F.action == "enable_shifts_notifications"))
async def enable_shifts_notifications(
        query: CallbackQuery,
        uow: UOWDep = UnitOfWork(),
):
    await toggle_notification_status(query, uow, enabled=True)


@router.callback_query(NotificationsCallback.filter(F.action == "disable_shifts_notifications"))
async def disable_shifts_notifications(
        query: CallbackQuery,
        uow: UOWDep = UnitOfWork(),
):
    await toggle_notification_status(query, uow, enabled=False)


async def toggle_notification_status(
        query: CallbackQuery,
        uow: UOWDep,
        enabled: bool
):
    user_id = query.from_user.id
    notification_id = NotificationsEnum.shifts.value

    existing_notification = await NotificationsService(uow).get_user_notification(
        schemas.GetUserNotificationSchema(user_id=user_id, notification_id=notification_id)
    )

    if existing_notification is None:
        create_notification_schema = schemas.CreateNotificationSchema(
            user_id=user_id,
            notification_id=notification_id,
            enabled=enabled,
        )
        await NotificationsService(uow).create_notification(create_notification_schema)
        action_message = "включено" if enabled else "выключено"
        return await query.answer(f"Уведомление создано и {action_message}")

    if existing_notification.enabled == enabled:
        action_message = "включено" if enabled else "выключено"
        return await query.answer(f"Уведомление уже {action_message}")

    toggle_notification_schema = schemas.ToggleNotificationSchema(
        user_id=user_id,
        notification_id=notification_id,
        enabled=enabled,
    )
    await NotificationsService(uow).toggle_notification(toggle_notification_schema)
    action_message = "включено" if enabled else "выключено"
    await query.answer(f"Уведомление о сменах {action_message}")
