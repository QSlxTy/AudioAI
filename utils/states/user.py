from aiogram.fsm.state import State, StatesGroup


class FSMStart(StatesGroup):
    start = State()


class FSMCreate(StatesGroup):
    choose_lang = State()
    choose_count_speakers = State()
    choose_words = State()

class FSMPromo(StatesGroup):
    menu_promo = State()

class FSMTariff(StatesGroup):
    get_email = State()