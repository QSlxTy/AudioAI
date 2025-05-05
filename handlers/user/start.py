import os
from datetime import datetime

from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.minute import get_minute_db
from integrations.database.models.user import update_user_db, get_user_db
from keyboards.other.menu_keyboard import main_menu_kb
from src.config import Configuration
from utils.aiogram_helper import seconds_to_hms
from utils.states.user import FSMStart


async def start_command(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_user_db({'telegram_id': message.from_user.id}, session_maker)
    os.makedirs(f'media/{message.from_user.id}', exist_ok=True)
    chat_member = await bot.get_chat_member(-1002257040885, message.from_user.id)
    # logger.info(f"Start command received from {message.from_user.id}")
    # if chat_member.status in ['member', 'administrator', 'creator']:
    await update_user_db(message.from_user.id, {'last_active': datetime.now()}, session_maker)
    await message.answer_photo(
        photo=Configuration.main_photo_path,
        caption='<b>Переводим аудио и видео в текст с помощью ИИ</b>\n\n'
                'Быстро, точно, дёшево. Попробуйте бесплатно!\n\n'
                '<b>Что мы предлагаем?</b>\n'
                '✅ Быстрая транскрибация аудио и видео\n'
                '✅ 30 минут бесплатной транскрибации\n'
                '✅ Поддержка файлов до <b>2GB</b>\n'
                '✅ Работаем с ссылками на YouTube, Яндекс.Диск, Google Drive\n'
                '✅ Дополнительно:\n'
                '- Саммари\n'
                '- Протокол встречи\n'
                '- Тайм-коды\n'
                '- Перечень задач\n'
                '- Анализ диалога\n',
        reply_markup=await main_menu_kb(user_info.is_admin)
    )
    await state.clear()
    await state.set_state(FSMStart.start)
    await state.update_data(lang='', count_speakers='', special_words='', path=[], duration=0, file_msg_id=[],
                            file_id=[], url_files=[], url_msg_id=[],
                            format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров',
                            format_summary=['Саммари'])
    return
    # await message.answer(
    #     text="📢 Для работы с ботом подпишитесь на наш канал <a href='https://t.me/lifesync_ai'>[GBA AI]</a>,"
    #          " а затем нажмите /start. Мы вас ждем! 😃"
    # )


async def main_menu(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_user_db({'telegram_id': call.from_user.id}, session_maker)

    os.makedirs(f'media/{call.from_user.id}', exist_ok=True)
    # chat_member = await bot.get_chat_member(-1002257040885, call.from_user.id)
    # if chat_member.status in ['member', 'administrator', 'creator']:
    await update_user_db(call.from_user.id, {'last_active': datetime.now()}, session_maker)
    await call.message.answer_photo(
        photo=Configuration.main_photo_path,
        caption='<b>Переводим аудио и видео в текст с помощью ИИ</b>\n\n'
                'Быстро, точно, дёшево. Попробуйте бесплатно!\n\n'
                '<b>Что мы предлагаем?</b>\n'
                '✅ Быстрая транскрибация аудио и видео\n'
                '✅ 30 минут бесплатной транскрибации\n'
                '✅ Поддержка файлов до <b>2GB</b>\n'
                '✅ Работаем с ссылками на YouTube, Яндекс.Диск, Google Drive\n'
                '✅ Дополнительно:\n'
                '- Саммари\n'
                '- Протокол встречи\n'
                '- Тайм-коды\n'
                '- Перечень задач\n'
                '- Анализ диалога\n',
        reply_markup=await main_menu_kb(user_info.is_admin)
    )
    await state.clear()
    await state.set_state(FSMStart.start)
    await state.update_data(lang='', count_speakers='', special_words='', path=[], duration=0, file_msg_id=[],
                            file_id=[], url_files=[], url_msg_id=[],
                            format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров',
                            format_summary=['Саммари'])

    # await call.message.answer(
    #     text="📢 Для работы с ботом подпишитесь на наш канал <a href='https://t.me/lifesync_ai'>[GBA AI]</a>,"
    #          " а затем нажмите /start. Мы вас ждем! 😃")


async def first_step_call(call: types.CallbackQuery, session_maker: sessionmaker, state: FSMContext):
    user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)
    os.makedirs(f'media/{call.from_user.id}', exist_ok=True)
    await update_user_db(call.from_user.id, {'last_active': datetime.now()}, session_maker)
    # chat_member = await bot.get_chat_member(-1002257040885, call.from_user.id)
    # if chat_member.status in ['member', 'administrator', 'creator']:
    await call.message.answer_photo(
        photo=Configuration.first_photo_url,
        caption=f'⏳ <b>Ваше оставшееся время:</b> {await seconds_to_hms(user_info.remaining_seconds)}\n'
                '❗️ Если не хватает минут, пополните их в Меню.\n\n'
                '<b>ШАГ 1: Загрузка файла</b>\n'
                '📂 Загрузите аудио или видео (до <b>2GB</b>)\n'
                '🔗 Или отправьте ссылку (YouTube, Яндекс.Диск, Google Drive)\n'
                '(Важно! Доступ по ссылке должен быть открыт)'
    )
    await state.set_state(FSMStart.start)
    await state.update_data(lang='', count_speakers='', special_words='', path=[], duration=0, file_msg_id=[],
                            file_id=[], url_files=[], url_msg_id=[],
                            format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров',
                            format_summary=['Саммари'])
    return
    # await call.message.answer(
    #     text="📢 Для работы с ботом подпишитесь на наш канал <a href='https://t.me/lifesync_ai'>[GBA AI]</a>,"
    #          " а затем нажмите /start. Мы вас ждем! 😃")


async def first_step_message(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    await state.set_state(FSMStart.start)
    user_info = await get_minute_db({'telegram_id': message.from_user.id}, session_maker)

    os.makedirs(f'media/{message.from_user.id}', exist_ok=True)
    await update_user_db(message.from_user.id, {'last_active': datetime.now()}, session_maker)
    # chat_member = await bot.get_chat_member(-1002257040885, message.from_user.id)
    # if chat_member.status in ['member', 'administrator', 'creator']:
    await message.answer_photo(
        photo=Configuration.first_photo_url,
        caption=f'⏳ <b>Ваше оставшееся время:</b> {await seconds_to_hms(user_info.remaining_seconds)}\n'
                '❗️ Если не хватает минут, пополните их в Меню.\n\n'
                '<b>ШАГ 1: Загрузка файла</b>\n'
                '📂 Загрузите аудио или видео (до <b>2GB</b>)\n'
                '🔗 Или отправьте ссылку (YouTube, Яндекс.Диск, Google Drive)\n'
                '(Важно! Доступ по ссылке должен быть открыт)'
    )
    await state.set_state(FSMStart.start)
    await state.update_data(lang='', count_speakers='', special_words='', path=[], duration=0, file_msg_id=[],
                            file_id=[], url_files=[], url_msg_id=[],
                            format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров',
                            format_summary=['Саммари'])

    # await message.answer(
    #     text="📢 Для работы с ботом подпишитесь на наш канал <a href='https://t.me/lifesync_ai'>[GBA AI]</a>,"
    #          " а затем нажмите /start. Мы вас ждем! 😃")


def register_start_handler(dp: Dispatcher):
    dp.message.register(start_command, Command('start'))
    dp.callback_query.register(main_menu, F.data == 'main_menu')
    dp.callback_query.register(first_step_call, F.data == 'first_step')
    dp.message.register(first_step_message, Command('transcribe'))
