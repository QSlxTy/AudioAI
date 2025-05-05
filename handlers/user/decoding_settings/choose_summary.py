from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from bot_start import logger
from keyboards.user.user_keyboard import choose_summary_kb
from src.big_text import prompts_list_txt


async def choose_summary(call: types.CallbackQuery, state: FSMContext):
    logger.info(f'Summary settings --> {call.from_user.id}')
    data = await state.get_data()
    msg = await data['msg'].edit_text(
        text=prompts_list_txt,
        reply_markup=await choose_summary_kb(data['format_summary'])
    )
    await state.update_data(msg=msg)


async def get_summary(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    list_summary = data['format_summary']
    if int(call.data.split(':')[1]) == 2:
        if 'Саммари' in list_summary:
            list_summary.remove('Саммари')
        else:
            list_summary.append('Саммари')
    if int(call.data.split(':')[1]) == 1:
        if 'Протокол встречи' in list_summary:
            list_summary.remove('Протокол встречи')
        else:
            list_summary.append('Протокол встречи')
    if int(call.data.split(':')[1]) == 4:
        if 'Анализ диалога' in list_summary:
            list_summary.remove('Анализ диалога')
        else:
            list_summary.append('Анализ диалога')
    if int(call.data.split(':')[1]) == 3:
        if 'Перечень действий' in list_summary:
            list_summary.remove('Перечень действий')
        else:
            list_summary.append('Перечень действий')
    msg = await data['msg'].edit_text(
        text=prompts_list_txt,
        reply_markup=await choose_summary_kb(data['format_summary'])
    )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_summary, F.data == 'format_summary')
    dp.callback_query.register(get_summary, F.data.startswith('choose_summary'))
