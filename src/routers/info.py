from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.filters import TextFilter
from src.keyboards.inline.rules import edit_rules
from src.routers.utils import format_rules_list_to_str
from src.services.rules import RulesService
from src.services.users import UsersService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.unitofwork import UnitOfWork

router = Router(name=__name__)


@router.message(Command("info"))
async def help_handler(message: Message):
    await message.answer(texts.help_text)


@router.message(TextFilter(texts.list_rules))
async def show_rules(message: Message, uow: UOWDep = UnitOfWork()):
    is_authorized = await UsersService(uow).check_rights(message.from_user.id, 50)
    edit_rules_keyboard = edit_rules if is_authorized else None

    reply_text = "Пусто"
    rules_list = await RulesService(uow).get_rules()
    if rules_list:
        reply_text = format_rules_list_to_str(rules_list)

    await message.answer(text=reply_text, reply_markup=edit_rules_keyboard)
