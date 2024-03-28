from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.filters import TextFilter
from src.keyboards.inline.notifications import notifications as notifications_kb, NotificationsCallback
from src.utils import texts

router = Router(name=__name__)


@router.message(TextFilter(texts.notifications))
async def take_shift(message: Message):
    await message.answer("Параметры уведомлений", reply_markup=notifications_kb)


@router.message(NotificationsCallback.filter(F.action == "get_shifts_notifications"))
async def get_shifts_notifications(query: CallbackQuery):
    ...
