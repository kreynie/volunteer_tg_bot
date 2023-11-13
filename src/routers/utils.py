from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.schemas.rules import RuleSchema

router = Router(name=__name__)


async def reset_user_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Завершено")


def format_rules_list_to_str(rules: list[RuleSchema]) -> str:
    result = ""
    current_rule_number = None

    for rule in rules:
        if '.' in rule.rule_number:  # subrule
            result += f"{rule.rule_number}) {rule.text}\n"
        else:
            if current_rule_number is not None:  # main rule
                result += "\n"
            result += f"{rule.rule_number}) {rule.text}\n"
            current_rule_number = rule.rule_number

    return result
