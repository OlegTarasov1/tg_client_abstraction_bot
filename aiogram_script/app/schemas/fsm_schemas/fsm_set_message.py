from aiogram.fsm.state import StatesGroup, State


class SetNewMessageFSM(StatesGroup):
    new_message_text = State()
