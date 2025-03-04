from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    INPUT_AREA = State()
    INPUT_ROOM = State()
    INPUT_BUDGET = State()
    INPUT_GEOGRAPHY = State()
    INPUT_STYLE = State()
    INPUT_INTERESTS = State()
