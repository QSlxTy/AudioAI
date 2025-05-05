from aiogram.fsm.state import State, StatesGroup


class FSMCreate(StatesGroup):
    go_create = State()
    get_photo = State()

class FSMMail(StatesGroup):
    get_email = State()
