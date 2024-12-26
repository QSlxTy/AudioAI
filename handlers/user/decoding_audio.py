import os
from datetime import datetime

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot, logger
from integrations.database.models.action import create_action_db
from integrations.database.models.minute import get_minute_db, update_minute_db
from integrations.database.models.user import update_user_db
from keyboards.user.user_keyboard import back_menu_kb
from utils.GPT.GPT import create_theses_from_transcription
from utils.URL import upload_yadisk_file
from utils.aiogram_helper import split_message


async def go_decoding(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)
    data = await state.get_data()
    if user_info.remaining_seconds < data['duration_sec']:
        await call.message.answer(
            text='<b>К сожалению, вам не хватает минут на балансе\n\n'
                 f'Минут у вас: <code>{user_info.remaining_seconds / 60}</code>\n'
                 f'Требуется минут: <code>{data["duration"]}</code>\n\n'
                 f'Баланс можно пополнить в главном меню 👉 /start</b>'
        )
        return

    await call.message.answer(
        text='<b>Спасибо! Я начал обработку файлов</b>'
    )

    for index, audio_file_path in enumerate(data['path']):
        try:
            decode_path = await upload_yadisk_file(bot, data['file_id'], audio_file_path, data['lang'],
                                                   data['count_speakers'],
                                                   data['special_words'],
                                                   data['format_decoding'], call.from_user.id,
                                                   session_maker)
            await state.update_data(decode_path=decode_path)
            user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)
            data = await state.get_data()
            await call.message.answer(
                text='<b>Отлично. Начинаю генерацию тезисов</b>'
            )
        except Exception as _ex:
            data = await state.get_data()
            logger.error(f'Decoding error {_ex} --> go_decoding_handler')
            try:
                os.remove(data['path'])
            except Exception as _ex:
                logger.error(f'Delete error {_ex} --> go_decoding_handler')
            await call.message.answer(
                text=f'<b>К сожалению во время расшифровки файла <code>{index + 1}</code> произошла ошибка\n\n'
                     'Минуты за него уже вернулись вам на баланс, продолжаю расшифровку остальных файлов</b>',
                reply_markup=await back_menu_kb()
            )
            continue
        try:
            gpt_output = await create_theses_from_transcription(data['format_summary'], data['decode_path'])
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f'<b>Обработка файла <code>{index + 1}</code> из <code>{len(data["path"])}</code> завершена\n\n'
                     f'Осталось файлов <code>{len(data["path"]) - index - 1}</code></b>'
            )
            await bot.send_document(
                chat_id=call.from_user.id,
                document=FSInputFile(decode_path),
                reply_to_message_id=data['file_msg_id'][index]
            )
            if len(gpt_output) > 4000:
                parts = await split_message(gpt_output)
                for part in parts:
                    await bot.send_message(
                        chat_id=call.from_user.id,
                        text=part,
                        reply_to_message_id=data['file_msg_id'][index]
                    )
            else:
                await bot.send_message(
                    chat_id=call.from_user.id, text=gpt_output,
                    reply_to_message_id=data['file_msg_id'][index],
                    reply_markup=await back_menu_kb()
                )
            await create_action_db(call.from_user.id,
                                   audio_file_path,
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
        except Exception as _ex:
            logger.error(f'Summary error {_ex} --> go_summary_handler')

            await call.message.answer(
                text=f'<b>К сожалению во время генерации тезисов для файла <code>{index + 1}</code> произошла ошибка\n\n'
                     'Минуты за него уже вернулись вам на баланс, продолжаю расшифровку остальных файлов</b>',
                reply_markup=await back_menu_kb()
            )
        finally:
            try:
                os.remove(decode_path)
            except Exception as _ex:
                logger.error(f'File already been deleted --> go_summary_handler')


def register_handler(dp: Dispatcher):
    dp.callback_query.register(go_decoding, F.data == 'go_decoding')
