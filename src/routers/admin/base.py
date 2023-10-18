from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.filters import TextFilter
from src.routers.event import get_shifts_history
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.middlewares import AuthorizedCommandsMiddleware
from src.utils.unitofwork import UnitOfWork
from .admin_keyboard import get_admin_keyboard
from .manage_rules import router as rules_manager_router
from .manage_users import router as users_manager_router

router = Router(name=__name__)
router.message.middleware(AuthorizedCommandsMiddleware(
    uow=UnitOfWork(),
    authority_level=50,
))
router.include_routers(rules_manager_router, users_manager_router)


@router.message(Command("admin"))
async def admin_panel(message: Message):
    await get_admin_keyboard(message)


@router.message(TextFilter(texts.list_shifts_text))
async def get_shift_history(message: Message, uow: UOWDep = UnitOfWork()):
    shift_logs = await get_shifts_history(uow=uow)
    await message.answer(shift_logs)
