from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import choose_lang_kb, go_decode_settings_kb
from utils.states.user import FSMCreate


async def choose_words(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_words)
    await call.message.answer(
        text='<b>Пожалуйста, введите специфические слова через запятую</b>',
        reply_markup=await choose_lang_kb()
    )


async def get_words(message: types.Message, state: FSMContext):
    await message.answer(
        text=f'<b>Запомнил количество спикеров:</b> <code>{message.text}</code>',
        reply_markup=await go_decode_settings_kb()
    )
    await state.update_data(special_words=message.text)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_words, F.data == 'add_word')
    dp.message.register(get_words, FSMCreate.choose_words, F.content_type == 'text')
