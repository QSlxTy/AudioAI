from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.tariff import get_all_tariff_db
from keyboards.user.user_keyboard import tariff_list_kb


async def tariff_info_call(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    tariffs = await get_all_tariff_db(session_maker)
    string_text = ''
    for tariff in tariffs:
        string_text += f'·Пакет <code>{tariff.tariff_name}</code> минут: <code>{tariff.price}</code> RUB\n'
    await state.get_data()
    await call.message.answer(
        text="💡 Хотите больше минут? Отличная идея! Вы можете приобрести их прямо сейчас.\n\n"
             "Все <b>купленные минуты</b> добавятся к вашему текущему балансу, чтобы у вас всегда было время для нужных задач!\n\n"
             f'{string_text}',
        reply_markup=await tariff_list_kb(session_maker)
    )


async def tariff_info_command(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    tariffs = await get_all_tariff_db(session_maker)
    string_text = ''
    for tariff in tariffs:
        string_text += f'·Пакет <code>{tariff.tariff_name}</code> минут: <code>{tariff.price}</code> RUB\n'
    await state.get_data()
    await message.answer(
        text="💡 Хотите больше минут? Отличная идея! Вы можете приобрести их прямо сейчас.\n\n"
             "Все <b>купленные минуты</b> добавятся к вашему текущему балансу, чтобы у вас всегда было время для нужных задач!\n\n"
             f'{string_text}',
        reply_markup=await tariff_list_kb(session_maker)
    )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(tariff_info_call, F.data == 'check_tariff')
    dp.message.register(tariff_info_command, Command('tarif'))
