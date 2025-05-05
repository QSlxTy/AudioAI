from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from bot_start import logger
from keyboards.user.user_keyboard import go_decode_settings_kb, choose_words_kb
from utils.states.user import FSMCreate


async def choose_words(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSMCreate.choose_words)
    logger.info(f'Words settings --> {call.from_user.id}')

    msg = await data['msg'].edit_text(
        text='🔤 ✍️ Укажите сложные термины, аббревиатуры, названия компаний (например: NVIDIA, ФПТ КП). '
             'Или выберите <b>автоопределение</b>.',
        reply_markup=await choose_words_kb()
    )
    await state.update_data(msg=msg)


async def get_words(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg = await data['msg'].edit_text(
        text=f'👍 <b>Отлично! Я запомнил ваши специфические слова:</b> <code>{message.text}</code>',
        reply_markup=await go_decode_settings_kb()
    )
    await state.update_data(special_words=message.text, msg=msg)


async def auto_words(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = await data['msg'].edit_text(
        text='✅ Вы выбрали <code>автоопределение</code>. Мы все настроим сами!',
        reply_markup=await go_decode_settings_kb()
    )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_words, F.data == 'add_word')
    dp.callback_query.register(auto_words, F.data == 'auto_words')
    dp.message.register(get_words, FSMCreate.choose_words, F.content_type == 'text')
