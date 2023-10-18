from aiogram.fsm.state import State, StatesGroup


class ManageUsersState(StatesGroup):
    addition = State()
    removal = State()


class ManageRulesState(StatesGroup):
    addition = State()
    removal = State()
    editing = State()
    editing_rule_id = State()
    rule_text = State()
