from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.filters import TextFilter
from src.keyboards.inline import EditRulesCallback
from src.routers.utils import reset_user_state
from src.schemas.rules import EditRuleSchema
from src.services.rules import RulesService
from src.utils import texts
from src.utils.dependencies import UOWDep
from src.utils.states import ManageRulesState
from src.utils.stickers_enum import MariAndHide
from src.utils.unitofwork import UnitOfWork

router = Router(name=__name__)


@router.message(TextFilter(texts.add_rule_text))
async def set_rule_addition_state(message: Message, state: FSMContext):
    await state.set_state(ManageRulesState.addition)
    await message.answer('Пиши текст правила. Для завершения или отмены нажми на кнопку снизу')


@router.message(ManageRulesState.addition, TextFilter(texts.done_text))
async def clear_rule_addition_state(message: Message, state: FSMContext):
    await reset_user_state(message, state)


@router.message(ManageRulesState.addition)
async def add_rule(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    if not message.text:
        return await message.answer("Мне нужен текст правила")
    await RulesService(uow).add_rule(message.text)
    await message.answer("Добавлено")
    await state.clear()


@router.message(TextFilter(texts.remove_rule_text))
async def set_removal_rule_state(message: Message, state: FSMContext):
    await state.set_state(ManageRulesState.removal)
    await message.answer("Пиши номер правила")


# @router.message(ManageRulesState.removal)
# async def remove_rule(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
#     if not message.text or not message.text.isdigit():
#         return await message.answer("Нужен номер правила")
#     await RulesService(uow).delete_rule(int(message.text))
#     await message.answer("Удалено")
#     await state.clear()


@router.callback_query(EditRulesCallback.filter(F.action == "edit"))
async def callback_edit_rules(query: CallbackQuery, state: FSMContext):
    await state.set_state(ManageRulesState.editing)
    message_text = query.message.text
    await query.message.edit_text(text=message_text)
    await query.message.answer(text='Дай номер правила. Для отмены введи "отмена"')


@router.message(ManageRulesState.editing)
@router.message(ManageRulesState.removal)
async def manage_rules(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    if not message.text or not message.text.isdigit():
        return await message.answer("Нужен номер правила")

    current_state = await state.get_state()
    if current_state == ManageRulesState.editing:
        await state.update_data(editing_rule_id=int(message.text))
        await state.set_state(ManageRulesState.rule_text)
        await message.answer("Теперь текст, на который нужно заменить\n"
                             'Если введен неверный номер, напиши "назад"\n'
                             'Для отмены введи "отмена"')
    elif current_state == ManageRulesState.removal:
        await RulesService(uow).delete_rule(int(message.text))
        await message.answer("Удалено")
        await state.clear()


# @router.message(ManageRulesState.editing)
# async def edit_rules_type_rule_id(message: Message, state: FSMContext):
#     message_cansel_text = "Мне нужен номер правила"
#     if not message.text:
#         return await message.answer(message_cansel_text)
#     if message.text.lower() == "отмена":
#         await state.clear()
#         return await message.answer("Редактирование отменено")
#     if not message.text.isdigit():
#         return await message.answer(message_cansel_text)
#     await state.update_data(editing_rule_id=int(message.text))
#     await state.set_state(ManageRulesState.rule_text)
#     await message.answer("Теперь текст, на который нужно заменить\n"
#                          'Если введен неверный номер, напиши "назад"\n'
#                          'Для отмены введи "отмена"')


@router.message(ManageRulesState.rule_text)
async def finish_edition_rules(message: Message, state: FSMContext, uow: UOWDep = UnitOfWork()):
    if not message.text:
        return await message.answer("Мне нужен текст правила")
    if message.text.lower() == "назад":
        await state.set_state(ManageRulesState.editing)
        await message.answer("Неряха. Дай нужный номер правила")
        return message.answer_sticker(sticker=MariAndHide.bonk)
    elif message.text.lower() == "отмена":
        await state.clear()
        return await message.answer("Редактирование отменено")

    rule_data = await state.get_data()
    await state.clear()
    rule = EditRuleSchema(id=rule_data["editing_rule_id"], text=message.text)
    returned_rule_id = await RulesService(uow).edit_rule(rule)
    await message.answer(f"Отредактировано {returned_rule_id}-ое правило")
