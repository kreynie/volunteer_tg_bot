from aiogram.fsm.state import State, StatesGroup


class GetForwardedUserIDState(StatesGroup):
    getting = State()


class ManageUsersState(StatesGroup):
    addition = State()
    removal = State()
