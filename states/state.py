from symtable import Class

from aiogram.fsm.state import State, StatesGroup

class AddGroup(StatesGroup):
    group_name = State()
    teacher_tg_id = State()
    scores = State()

class AddTeacher(StatesGroup):
    tg_id = State()
    name = State()

class EditTeacher(StatesGroup):
    tg_id = State()
    name = State()


class Misstake(StatesGroup):
    tg_id = State()
    problem = State()
    group_name = State()
    scores = State()