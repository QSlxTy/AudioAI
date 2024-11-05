from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import choose_summary_kb
from src.big_text import prompts_list_txt


async def choose_summary(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text=prompts_list_txt,
            reply_markup=await choose_summary_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text=prompts_list_txt,
            reply_markup=await choose_summary_kb()
        )
    await state.update_data(msg=msg)


# async def get_summary(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     if '1' in call.data:
#         format_summary = 'Протокол встречи'
#     elif '2' in call.data:
#         format_summary = 'Краткая выжимка'
#     elif '3' in call.data:
#         format_summary = 'Анализ диалога'
#     else:
#         format_summary = 'Перечень действий'
#
#     try:
#         msg = await data['msg'].edit_text(
#             text=
#             f'<b>Запомнил формат расшифровки:</b> <code>{format_summary}</code>',
#             reply_markup=await go_decode_settings_kb()
#         )
#     except (TelegramBadRequest, KeyError) as _ex:
#         await call.message.delete()
#         msg = await call.message.answer(
#             text=
#             f'<b>Запомнил формат расшифровки:</b> <code>{format_summary}</code>',
#             reply_markup=await go_decode_settings_kb()
#         )
#     await state.update_data(msg=msg, format_summary=format_summary)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_summary, F.data == 'format_summary')
    # dp.callback_query.register(get_summary, F.data.startswith('choose_summary'))
