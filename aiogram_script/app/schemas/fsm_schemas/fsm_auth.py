from aiogram.fsm.state import StatesGroup, State


class AuthorizationFSM(StatesGroup):
    data_type = State()
    data = State()
