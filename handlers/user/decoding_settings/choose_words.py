from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import choose_lang_kb, go_decode_settings_kb
from utils.states.user import FSMCreate


async def choose_words(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_words)
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Пожалуйста, введите специфические слова через запятую</b>',
            reply_markup=await choose_lang_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Пожалуйста, введите специфические слова через запятую</b>',
            reply_markup=await choose_lang_kb()
        )
    await state.update_data(msg=msg)


async def get_words(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    try:
        msg = await data['msg'].edit_text(
            text=f'<b>Запомнил слова:</b> <code>{message.text}</code>',
            reply_markup=await go_decode_settings_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await message.delete()
        msg = await message.answer(
            text=f'<b>Запомнил количество спикеров:</b> <code>{message.text}</code>',
            reply_markup=await go_decode_settings_kb()
        )
    await state.update_data(msg=msg, special_words=message.text)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_words, F.data == 'add_word')
    dp.message.register(get_words, FSMCreate.choose_words, F.content_type == 'text')
