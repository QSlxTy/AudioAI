from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import go_decode_settings_kb, choose_decoding_kb
from utils.states.user import FSMCreate


async def choose_decoding(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_lang)
    await call.message.answer(
        text='<b>1. Расшифровка с тайм-кодами и разбиением на спикеров\n'
             '2. Расшифровка всего текста без разбивки</b>',
        reply_markup=await choose_decoding_kb()
    )


async def get_decoding(call: types.CallbackQuery, state: FSMContext):
    if '1' in call.data:
        format_decoding = 'Расшифровка с тайм-кодами и разбиением на спикеров'
    else:
        format_decoding = 'Расшифровка всего текста без разбивки'

    await call.message.answer(
        text=f'<b>Запомнил формат расшифровки:</b> <code>{format_decoding}</code>',
        reply_markup=await go_decode_settings_kb()
    )
    await state.update_data(format_decoding=format_decoding)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_decoding, F.data == 'format_decode')
    dp.callback_query.register(get_decoding, FSMCreate.choose_lang, F.data.startswith('choose_format_decode'))
