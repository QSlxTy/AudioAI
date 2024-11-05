import asyncio
import logging
import os
from datetime import datetime, timedelta

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.action import create_action_db
from integrations.database.models.minute import get_minute_db, update_minute_db
from integrations.database.models.user import update_user_db
from keyboards.user.user_keyboard import back_menu_kb, choose_summary_kb
from src.big_text import prompts_list_txt
from utils.GPT.GPT import create_theses_from_transcription
from utils.URL import upload_yadisk_file
from utils.aiogram_helper import split_message
from utils.replicate_api import replicate_func


async def go_decoding(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)
    data = await state.get_data()
    if user_info.remaining_seconds < data['duration_sec']:
        try:
            msg = await data['msg'].edit_text(
                text='<b>К сожалению, вам не хватает минут на балансе\n\n'
                     f'Минут у вас: <code>{user_info.remaining_seconds / 60}</code>\n'
                     f'Требуется минут: <code>{data["duration"]}</code>\n\n'
                     f'Баланс можно пополнить в главном меню 👉 /start</b>'
            )
        except (TelegramBadRequest, KeyError) as _ex:
            await call.message.delete()
            msg = await call.message.answer(
                text='<b>К сожалению, вам не хватает минут на балансе\n\n'
                     f'Минут у вас: <code>{user_info.remaining_seconds / 60}</code>\n'
                     f'Требуется минут: <code>{data["duration"]}</code>\n\n'
                     f'Баланс можно пополнить в главном меню 👉 /start</b>'
            )
        await state.update_data(msg=msg)
    else:
        msg = await data['msg'].edit_text(
            text='<b>Я начал обработку файла, и это займет примерно 5-10 минут.</b>'
        )
        await asyncio.sleep(2)
        data = await state.get_data()
        try:
            if data['size'] > 20971520:
                file, decode_path = await upload_yadisk_file(data['path'], data['lang'], data['count_speakers'],
                                                             data['special_words'],
                                                             data['format_decoding'], call.from_user.id,
                                                             session_maker)
            else:
                file, decode_path = await replicate_func(data['path'], data['lang'], data['count_speakers'],
                                                         data['special_words'],
                                                         data['format_decoding'], call.from_user.id, session_maker)
            os.remove(file)
            await state.update_data(path=file, decode_path=decode_path)
            await msg.delete()
            await bot.send_document(chat_id=call.from_user.id,
                                    document=FSInputFile(decode_path))
            if file is not None:
                msg = await call.message.answer(
                    text=prompts_list_txt,
                    reply_markup=await choose_summary_kb()
                )
            await state.update_data(msg=msg)
        except Exception as _ex:
            data = await state.get_data()
            logging.error(f'Decoding error {_ex} --> go_decoding_other_files_handler')
            try:
                os.remove(data['path'])
            except Exception as _ex:
                logging.error(f'File already been deleted --> go_decoding_other_files_handler')
            await call.message.answer(
                text='<b>К сожалению во время расшифровки произошла ошибка\n'
                     'Минуты уже вернулись вам на баланс</b>',
                reply_markup=await back_menu_kb()
            )


async def go_summary(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)
    data = await state.get_data()
    three_days_ago = datetime.now() - timedelta(days=3)
    file_date = datetime.strptime(data['decode_path'].split('/')[2].split('_')[0], "%Y-%m-%d")
    if file_date < three_days_ago:
        msg = await data['msg'].edit_text(text='<b>Мы хотим сообщить вам, что прошло более 3 дней с момента '
                                               'загрузки вашего файла, и в соответствии с нашей политикой хранения '
                                               'данных, он был автоматически удален с нашего сервера.</b>',
                                          reply_markup=back_menu_kb())
        await state.update_data(msg=msg)
    else:
        msg = await data['msg'].edit_text(text='<b>Отлично. Начинаю генерацию тезисов</b>')
        try:
            gpt_output = await create_theses_from_transcription(data['format_summary'], data['decode_path'])
            await msg.delete()

            if len(gpt_output) > 4000:
                parts = await split_message(gpt_output)
                for part in parts:
                    await bot.send_message(chat_id=call.from_user.id, text=part)
            else:
                await bot.send_message(chat_id=call.from_user.id, text=gpt_output, reply_markup=await back_menu_kb())
            os.remove(data['decode_path'])
            await create_action_db(call.from_user.id,
                                   data['path'],
                                   data['duration_sec'],
                                   data['lang'],
                                   data['count_speakers'],
                                   data['special_words'],
                                   data['format_decoding'],
                                   data['format_summary'],
                                   session_maker)

            await update_minute_db(call.from_user.id,
                                   {'remaining_seconds': user_info.remaining_seconds - data['duration_sec']},
                                   session_maker)
            await update_user_db(call.from_user.id, {'last_active': datetime.now()}, session_maker)
            await state.clear()
        except Exception as _ex:
            data = await state.get_data()
            logging.error(f'GPT error {_ex} --> go_summary_other_files_handler')
            try:
                os.remove(data['decode_path'])
            except Exception as _ex:
                logging.error(f'File already been deleted --> go_summary_handler')
            await call.message.answer(
                text='<b>К сожалению во время генерации тезисов произошла ошибка\n'
                     'Минуты уже вернулись вам на баланс</b>',
                reply_markup=await back_menu_kb()
            )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(go_decoding, F.data == 'go_other_decoding')
    dp.callback_query.register(go_summary, F.data.startswith('choose_summary'))
