from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import choose_summary_kb, go_decode_settings_kb
from src.big_text import prompts_list_txt


async def choose_summary(call: types.CallbackQuery):
    await call.message.answer(
        text=prompts_list_txt,
        reply_markup=await choose_summary_kb()
    )


async def get_summary(call: types.CallbackQuery, state: FSMContext):
    if '1' in call.data:
        format_summary = 'Протокол встречи'
    elif '2' in call.data:
        format_summary = 'Краткая выжимка'
    elif '3' in call.data:
        format_summary = 'Анализ диалога'
    else:
        format_summary = 'Перечень действий'

    await call.message.answer(
        text=
        f'<b>Запомнил формат расшифровки:</b> <code>{format_summary}</code>',
        reply_markup=await go_decode_settings_kb()
    )
    await state.update_data(format_summary=format_summary)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_summary, F.data == 'format_summary')
    dp.callback_query.register(get_summary, F.data.startswith('choose_summary'))
