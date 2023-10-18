from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.filters import TextFilter
from src.keyboards.inline import ListShiftsCallback, paginator
from src.routers.event import format_shifts_history
from src.schemas.sort import QueryOrderBySchema
from src.services.shifts import ShiftsService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.unitofwork import UnitOfWork

router = Router(name=__name__)


@router.message(TextFilter(texts.list_shifts_text))
async def get_shift_history(message: Message, uow: UOWDep = UnitOfWork()):
    await display_shift_history(message, uow, page_num=0, edit_message=False)


@router.callback_query(ListShiftsCallback.filter(F.action.in_([texts.previous_page_action, texts.next_page_action])))
async def list_shifts_callback(
        query: CallbackQuery,
        callback_data: ListShiftsCallback,
        uow: UOWDep = UnitOfWork(),
):
    page_num = callback_data.page
    total_pages = callback_data.total_pages

    if callback_data.action == "next" and page_num < total_pages:
        page_num += 1
    elif callback_data.action == "previous" and page_num > 0:
        page_num -= 1

    await display_shift_history(query.message, uow, page_num)


async def display_shift_history(
        message: Message,
        uow: UOWDep,
        page_num: int,
        edit_message: bool = True,
):
    shift_logs = await ShiftsService(uow).get_shift_history()
    shift_logs_len = len(shift_logs)
    total_pages = (shift_logs_len - 1) // 10

    start_index = page_num * 10
    end_index = min((page_num + 1) * 10, shift_logs_len)

    user_shifts_text = format_shifts_history(
        shift_logs[start_index:end_index],
        number=end_index,
        offset=start_index,
        overall_amount=shift_logs_len,
    )

    pagination_buttons = paginator(page=page_num, total_pages=total_pages)
    if edit_message:
        return await message.edit_text(user_shifts_text, reply_markup=pagination_buttons)
    await message.answer(user_shifts_text, reply_markup=pagination_buttons)
