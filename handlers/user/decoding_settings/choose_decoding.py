from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import go_decode_settings_kb, choose_decoding_kb
from utils.states.user import FSMCreate


async def choose_decoding(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_lang)
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>1. Расшифровка с тайм-кодами и разбиением на спикеров\n'
                 '2. Расшифровка всего текста без разбивки</b>',
            reply_markup=await choose_decoding_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>1. Расшифровка с тайм-кодами и разбиением на спикеров\n'
                 '2. Расшифровка всего текста без разбивки</b>',
            reply_markup=await choose_decoding_kb()
        )
    await state.update_data(msg=msg)


async def get_decoding(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if '1' in call.data:
        format_decoding = 'Расшифровка с тайм-кодами и разбиением на спикеров'
    else:
        format_decoding = 'Расшифровка всего текста без разбивки'

    try:
        msg = await data['msg'].edit_text(
            text=f'<b>Запомнил формат расшифровки:</b> <code>{format_decoding}</code>',
            reply_markup=await go_decode_settings_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text=f'<b>Запомнил формат расшифровки:</b> <code>{format_decoding}</code>',
            reply_markup=await go_decode_settings_kb()
        )
    await state.update_data(msg=msg, format_decoding=format_decoding)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_decoding, F.data == 'format_decode')
    dp.callback_query.register(get_decoding, FSMCreate.choose_lang, F.data.startswith('choose_format_decode'))
