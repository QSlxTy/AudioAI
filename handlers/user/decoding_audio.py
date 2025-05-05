import os
from datetime import datetime

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot, logger
from integrations.database.models.action import create_action_db
from integrations.database.models.errors import create_error_db
from integrations.database.models.minute import get_minute_db, update_minute_db
from integrations.database.models.user import update_user_db
from keyboards.user.user_keyboard import back_menu_kb, choose_summary_kb, end_kb
from utils.GPT.GPT import create_theses_from_transcription
from utils.URL import upload_yadisk_file
from utils.aiogram_helper import seconds_to_hms
from utils.states.user import FSMStart


async def go_decoding(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    if not os.path.exists(f'media/{call.from_user.id}'):
        os.makedirs(f'media/{call.from_user.id}', exist_ok=True)
    user_info = await get_minute_db({'telegram_id': call.from_user.id}, session_maker)
    data = await state.get_data()
    if user_info.remaining_seconds < data['duration']:
        await call.message.answer(
            text=f"🙁 У вас осталось: <code>{await seconds_to_hms(int(user_info.remaining_seconds))}</code> минут.\n"
                 f"Для выполнения действия требуется: <code>{await seconds_to_hms(int(data['duration']))}</code> минут.\n\n"
                 "Не беда! Пополните <b>баланс</b> в главном меню 👉 /start, и мы продолжим работу. 💪"
        )

        for media_dir in os.listdir(f'media/{call.from_user.id}'):
            os.remove(f'media/{call.from_user.id}/{media_dir}')

        return
    if not data['format_summary']:
        await call.message.answer(
            text="⚙️ Пожалуйста, выберите <b>формат расшифровки</b>, чтобы мы могли продолжить. "
                 "Если нужна помощь — просто напишите нам!",
            reply_markup=await choose_summary_kb(data['format_summary'])
        )
        return
    await call.message.answer(
        text="🔄 Начинаю обработку ваших файлов. Это займет немного времени. Спасибо за ваше терпение! 🙌"
    )

    for index, file_id in enumerate(data['file_id']):
        file = await bot.get_file(file_id,
                                  request_timeout=300)
        audio_file_path = file.file_path.replace('\\', '/')
        logger.info(f'Decode file path --> {audio_file_path}')
        logger.info(f'Start upload bucket --> {call.from_user.id}')
        decode_path = await upload_yadisk_file(file_id, audio_file_path, data['lang'],
                                               data['count_speakers'],
                                               data['special_words'],
                                               data['format_decoding'], call.from_user.id,
                                               session_maker)
        logger.info(f'End upload bucket --> {call.from_user.id}')
        if decode_path is None:
            await create_error_db(call.from_user.id, 'Decoding file error', 'decoding_audio',
                                  'Error for decoding audio',
                                  session_maker)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"😔 Ой, произошла ошибка при расшифровке файла <code>{index + 1}</code> из "
                     f"<code>{len(data['file_id'])}</code>.\n\n"
                     "Но не волнуйтесь! <b>Минуты за этот файл</b> уже вернулись на ваш баланс. "
                     "А мы продолжаем работу с остальными файлами! 🚀",
                reply_to_message_id=data['file_msg_id'][index],
                reply_markup=await back_menu_kb()
            )
            continue
        try:
            logger.info(f'Start Create theses --> {call.from_user.id}')
            list_doc = await create_theses_from_transcription(call.from_user.id, data['format_summary'], decode_path)
            logger.info(f'End Create theses --> {call.from_user.id}')
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"✅ Обработка файла <code>{index + 1}</code> из <code>{len(data['file_id'])}</code> завершена! "
                     f"🎉 Спасибо за ожидание.\n\n"
                     f'Осталось файлов <code>{len(data["file_id"]) - index - 1}</code>'
            )
            await bot.send_document(
                chat_id=call.from_user.id,
                document=FSInputFile(decode_path),
                caption='<b>Расшифровка аудио</b>',
                reply_to_message_id=data['file_msg_id'][index]
            )
            for summary_index, doc in enumerate(list_doc):
                await bot.send_document(
                    chat_id=call.from_user.id,
                    document=FSInputFile(doc),
                    caption=f'<b>Тезисы в формате <code>{data["format_summary"][summary_index]}</code></b>',
                    reply_to_message_id=data['file_msg_id'][index]
                )
                os.remove(doc)
            if index + 1 != len(data['file_id']):
                await bot.send_message(
                    chat_id=call.from_user.id,
                    text=f'<b>Продолжаю расшифровку остальных файлов ⏱️</b>'
                )
            await update_user_db(call.from_user.id, {'last_active': datetime.now()}, session_maker)
            await update_minute_db(call.from_user.id,
                                   {'remaining_seconds': user_info.remaining_seconds - data['duration']},
                                   session_maker)
            logger.info(f'End Decoding --> {call.from_user.id}')
        except Exception as _ex:
            logger.error(f'Summary error {_ex} --> go_summary_handler')
            await create_error_db(call.from_user.id, 'GPT file error', 'decoding_audio', str(_ex), session_maker)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f'😔 Ой, произошла ошибка при генерации тезисов для файла <code>{index + 1}</code> из '
                     f'<code>{len(data["file_id"])}</code>\n\n'
                     "Но не волнуйтесь! <b>Минуты за этот файл</b> уже вернулись на ваш баланс. "
                     "А мы продолжаем работу с остальными файлами! 🚀",
                reply_to_message_id=data['file_msg_id'][index],
                reply_markup=await back_menu_kb()
            )
        finally:
            try:
                os.remove(decode_path)
            except Exception as _ex:
                logger.error(f'File already been deleted --> go_summary_handler')

    for index, file_path in enumerate(data['url_files']):
        logger.info(f'Start decode urls --> {call.from_user.id}')
        logger.info(f'Start upload bucket --> {call.from_user.id}')
        decode_path = await upload_yadisk_file(
            file_path.split('/')[-1], file_path, data['lang'],
            data['count_speakers'],
            data['special_words'],
            data['format_decoding'], call.from_user.id,
            session_maker
        )
        logger.info(f'End upload bucket --> {call.from_user.id}')
        if decode_path is None:
            await create_error_db(call.from_user.id, 'Decoding url error', 'decoding_audio', 'Error for decoding audio',
                                  session_maker)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"😔 Ой, произошла ошибка при расшифровке ссылки <code>{index + 1}</code>\n\n"
                     "Но не волнуйтесь! <b>Минуты за этот файл</b> уже вернулись на ваш баланс. "
                     "А мы продолжаем работу с остальными файлами! 🚀",
                reply_to_message_id=data['url_msg_id'][index],
                reply_markup=await back_menu_kb()
            )
            continue
        try:
            logger.info(f'Start Create theses --> {call.from_user.id}')
            list_doc = await create_theses_from_transcription(call.from_user.id, data['format_summary'], decode_path)
            logger.info(f'End Create theses --> {call.from_user.id}')
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"✅ Обработка ссылки <code>{index + 1}</code> из <code>{len(data['url_files'])}</code> завершена! "
                     f"🎉 Спасибо за ожидание.\n\n"
                     f'Осталось ссылок <code>{len(data["url_files"]) - index - 1}</code>'
            )
            await bot.send_document(
                chat_id=call.from_user.id,
                document=FSInputFile(decode_path),
                caption='<b>Расшифровка аудио</b>',
                reply_to_message_id=data['url_msg_id'][index]
            )

            for summary_index, doc in enumerate(list_doc):
                await bot.send_document(
                    chat_id=call.from_user.id,
                    document=FSInputFile(doc),
                    caption=f'<b>Тезисы в формате <code>{data["format_summary"][summary_index]}</code></b>',
                    reply_to_message_id=data['url_msg_id'][index]
                )
                os.remove(doc)
            if index + 1 != len(data['url_files']):
                await bot.send_message(
                    chat_id=call.from_user.id,
                    text=f'<b>Продолжаю расшифровку остальных ссылок ⏱️</b>'
                )
            await update_user_db(call.from_user.id, {'last_active': datetime.now()}, session_maker)
            await update_minute_db(call.from_user.id,
                                   {'remaining_seconds': user_info.remaining_seconds - data['duration']},
                                   session_maker)
            logger.info(f'End Decoding --> {call.from_user.id}')
        except Exception as _ex:
            logger.error(f'Summary error {_ex} --> go_summary_handler')
            await create_error_db(call.from_user.id, 'GPT url error', 'decoding_audio', str(_ex),
                                  session_maker)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f'😔 Ой, произошла ошибка при генерации тезисов для ссылки <code>{index + 1}</code>\n\n'
                     "Но не волнуйтесь! <b>Минуты за эту ссылку</b> уже вернулись на ваш баланс. "
                     "А мы продолжаем работу с остальными ссылками! 🚀",
                reply_to_message_id=data['url_msg_id'][index],
                reply_markup=await back_menu_kb()
            )
        finally:
            try:
                os.remove(decode_path)
            except Exception as _ex:
                logger.error(f'File already been deleted --> go_summary_handler')
    await call.message.answer(
        text="🥳 Все медиафайлы успешно <b>расшифрованы</b>! Отличная работа, мы с вами команда! 🚀",
        reply_markup=await end_kb()
    )
    await create_action_db(
        call.from_user.id,
        len(data['url_files']) + len(data['file_id']),
        data['duration'],
        data['lang'],
        data['count_speakers'],
        data['special_words'],
        data['format_decoding'],
        str(data['format_summary']).replace("[", "").replace("]", "").replace("'", ""),
        session_maker
    )
    await state.set_state(FSMStart.start)
    await state.update_data(lang='', count_speakers='', special_words='', path=[], duration=0, file_msg_id=[],
                            file_id=[], url_files=[],
                            format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров',
                            format_summary=['Саммари'])


def register_handler(dp: Dispatcher):
    dp.callback_query.register(go_decoding, F.data == 'go_decoding')
