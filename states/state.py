from aiogram.fsm.state import State, StatesGroup

class AddGroup(StatesGroup):
    group_name = State()
    teacher_tg_id = State()