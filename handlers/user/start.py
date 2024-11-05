from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.minute import get_minute_db
from keyboards.other.menu_keyboard import main_menu_kb
from utils.aiogram_helper import seconds_to_hms
from utils.states.user import FSMStart


async def start_command(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    await state.set_state(FSMStart.start)
    data = await state.get_data()
    user_info = await get_minute_db({'telegram_id': message.from_user.id}, session_maker)
    try:
        await data['msg'].delete()
    except KeyError:
        pass
    msg = await message.answer(
        text='<b>Добро пожаловать! 👋\n\n'
             f'Оставшиеся время: <code>{await seconds_to_hms(user_info.remaining_seconds)}</code>\n\n'
             'Пожалуйста, загрузите аудио или видео файл для расшифровки.\n\n'
             'Поддерживаемые форматы:\n'
             'Аудио:  m4a, m4b, m4p, m4r, mp3, aac, ac3, wav, alac, '
             'flac, flv, wma, amr, mpga, ogg, oga, mogg, 8svx, aif, '
             'ape, au, dss, opus, qcp, tta, voc, wv.\n\n'
             'Видео: m4p, m4v, webm, mts, m2ts, ts, mov, mp2, mxf.</b>',
        reply_markup=await main_menu_kb()
    )
    await message.delete()
    await state.update_data(msg=msg)


async def main_menu(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    await state.set_state(FSMStart.start)
    user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)

    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Добро пожаловать! 👋\n\n'
                 f'Оставшиеся время: <code>{await seconds_to_hms(user_info.remaining_seconds)}</code>\n\n'
                 'Пожалуйста, загрузите аудио или видео файл для расшифровки.\n\n'
                 'Поддерживаемые форматы:\n'
                 'Аудио:  m4a, m4b, m4p, m4r, mp3, aac, ac3, wav, alac, '
                 'flac, flv, wma, amr, mpga, ogg, oga, mogg, 8svx, '
                 'aif, ape, au, dss, opus, qcp, tta, voc, wv.\n\n'
                 'Видео: m4p, m4v, webm, mts, m2ts, ts, mov, mp2, mxf.</b>',
            reply_markup=await main_menu_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Добро пожаловать! 👋\n\n'
                 f'Оставшиеся время: <code>{await seconds_to_hms(user_info.remaining_seconds)}</code>\n\n'
                 'Пожалуйста, загрузите аудио или видео файл для расшифровки.\n\n'
                 'Поддерживаемые форматы:\n'
                 'Аудио:  m4a, m4b, m4p, m4r, mp3, aac, ac3, wav, alac, '
                 'Xflac, flv, wma, amr, mpga, ogg, oga, mogg, 8svx, '
                 'aif, ape, au, dss, opus, qcp, tta, voc, wv.\n\n'
                 'Видео: m4p, m4v, webm, mts, m2ts, ts, mov, mp2, mxf.</b>',
            reply_markup=await main_menu_kb()
        )

    await state.update_data(msg=msg)


def register_start_handler(dp: Dispatcher):
    dp.message.register(start_command, Command('start'))
    dp.callback_query.register(main_menu, F.data == 'main_menu')
