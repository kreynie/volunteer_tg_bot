from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.filters import TextFilter
from src.filters.rule_number import is_valid_rule_number
from src.keyboards.inline.rules import EditRulesCallback
from src.keyboards.reply.reset import reset_state
from src.routers.admin.admin_keyboard import get_admin_keyboard
from src.routers.utils import reset_user_state
from src.schemas.rules import AddRuleSchema, EditRuleSchema
from src.services.rules import RulesService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.states import ManageRulesState
from src.utils.stickers_enum import MariAndHide
from src.utils.unitofwork import UnitOfWork

router = Router(name=__name__)


@router.message(TextFilter(texts.add_rule_text))
@router.message(TextFilter(texts.remove_rule_text))
async def set_removal_rule_state(message: Message, state: FSMContext):
    rule_action = message.text
    if rule_action == texts.add_rule_text:
        await state.set_state(ManageRulesState.addition)
    else:
        await state.set_state(ManageRulesState.removal)
    await message.answer("Пиши номер правила. Для отмены нажми на кнопку снизу", reply_markup=reset_state)


@router.callback_query(EditRulesCallback.filter(F.action == "edit"))
async def callback_edit_rules(query: CallbackQuery, state: FSMContext):
    await state.set_state(ManageRulesState.editing)
    message_text = query.message.text
    await query.message.edit_text(text=message_text)
    await query.message.answer(text="Дай номер правила. Для отмены кнопка снизу", reply_markup=reset_state)


@router.message(ManageRulesState.addition, TextFilter(texts.done_text))
@router.message(ManageRulesState.editing, TextFilter(texts.done_text))
@router.message(ManageRulesState.removal, TextFilter(texts.done_text))
@router.message(ManageRulesState.rule_text, TextFilter(texts.done_text))
async def clear_rule_addition_state(message: Message, state: FSMContext):
    await reset_user_state(message, state)
    await get_admin_keyboard(message)


@router.message(ManageRulesState.addition)
@router.message(ManageRulesState.editing)
@router.message(ManageRulesState.removal)
async def manage_rules(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    if not message.text or not is_valid_rule_number(message.text):
        return await message.answer("Нужен номер правила")

    current_state = await state.get_state()
    if current_state == ManageRulesState.removal:
        await RulesService(uow).delete_rule(message.text)
        await message.answer("Удалено")
        return await state.clear()
    await state.update_data(managing_rule_number=message.text, previous_state=current_state)
    await state.set_state(ManageRulesState.rule_text)
    await message.answer("Теперь отправь текст.\n"
                         'Если введен неверный номер, напиши "назад"')


@router.message(ManageRulesState.rule_text)
async def finish_editing_rules(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    cancel = await cancel_editing_rule(message, state)
    if cancel is True:
        return

    rule_data = await state.get_data()
    rule_action = rule_data.get("previous_state", None)
    await state.clear()
    rule_number = rule_data["managing_rule_number"]
    rule_text = message.text
    if rule_action == ManageRulesState.addition:
        rule = AddRuleSchema(rule_number=rule_number, text=rule_text)
        action_message = "Добавлено {rule_number}-ое правило"
    else:
        rule = EditRuleSchema(rule_number=rule_number, text=rule_text)
        action_message = "Отредактировано {rule_number}-ое правило"

    service = RulesService(uow)
    returned_rule_number = await service.add_rule(rule) \
        if rule_action == ManageRulesState.addition \
        else await service.edit_rule(rule)
    await message.answer(action_message.format(rule_number=returned_rule_number))
    await get_admin_keyboard(message)


async def cancel_editing_rule(message: Message, state: FSMContext) -> bool:
    if not message.text:
        return bool(await message.answer("Мне нужен текст правила"))
    rule_data = await state.get_data()
    rule_action = rule_data.get("previous_state", None)
    if message.text.lower() == "назад":
        await state.set_state(rule_action)
        await message.answer_sticker(sticker=MariAndHide.bonk)
        return bool(await message.answer("Неряха. Дай нужный номер правила"))
    return False
