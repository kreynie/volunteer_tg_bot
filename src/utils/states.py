from aiogram.fsm.state import State, StatesGroup


class ManageUsersState(StatesGroup):
    addition = State()
    addition_moderator_id = State()
    editing = State()
    editing_choose_field = State()
    editing_chosen_field = State()
    removal = State()


class ManageRulesState(StatesGroup):
    addition = State()
    removal = State()
    editing = State()
    managing_rule_number = State()
    rule_text = State()
    previous_state = State()
