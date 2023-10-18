from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.utils.middlewares import AuthorizedCommandsMiddleware
from src.utils.unitofwork import UnitOfWork
from .admin_keyboard import get_admin_keyboard
from .manage_rules import router as rules_manager_router
from .manage_users import router as users_manager_router
from .manage_shifts import router as shifts_manager_router

router = Router(name=__name__)
router.message.middleware(AuthorizedCommandsMiddleware(
    uow=UnitOfWork(),
    authority_level=50,
))
router.include_routers(
    rules_manager_router,
    users_manager_router,
    shifts_manager_router,
)


@router.message(Command("admin"))
async def admin_panel(message: Message):
    await get_admin_keyboard(message)
