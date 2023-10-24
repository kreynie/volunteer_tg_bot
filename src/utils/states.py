from aiogram.fsm.state import State, StatesGroup


class ManageUsersState(StatesGroup):
    addition = State()
    removal = State()


class ManageRulesState(StatesGroup):
    addition = State()
    removal = State()
    editing = State()
    managing_rule_number = State()
    rule_text = State()
    previous_state = State()
