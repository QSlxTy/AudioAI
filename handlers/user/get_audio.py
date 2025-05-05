import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot_start import bot, logger
from integrations.database.models.errors import create_error_db
from keyboards.other.menu_keyboard import decoding_menu_kb, other_settings_kb
from keyboards.user.user_keyboard import cancel_kb
from src.config import Configuration
from utils.aiogram_helper import seconds_to_hms, get_duration_document
from utils.google_drive import get_google_file
from utils.states.user import FSMStart
from utils.yandex_drive import get_yandex_file
from utils.youtube_drive import get_youtube_file
from utils.rutube_download import get_rutube_file

async def get_audio(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    if not os.path.exists(f'media/{message.from_user.id}'):
        os.makedirs(f'media/{message.from_user.id}', exist_ok=True)
    await message.answer('Начинаю загрузку медиафайла ⬇️')
    if message.video:
        logger.info(
            f'Get video | ID --> {message.from_user.id}')
        duration = message.video.duration
        data['file_id'].append(message.video.file_id)
        data['file_msg_id'].append(message.message_id)
        await state.update_data(file_msg_id=data['file_msg_id'], file_id=data['file_id'])
    elif message.audio:
        logger.info(
            f'Get audio | ID --> {message.from_user.id}')
        duration = message.audio.duration
        data['file_id'].append(message.audio.file_id)
        data['file_msg_id'].append(message.message_id)
        await state.update_data(file_msg_id=data['file_msg_id'], file_id=data['file_id'])
    elif message.video_note:
        logger.info(
            f'Get video note | ID --> {message.from_user.id}')
        duration = message.video_note.duration
        data['file_id'].append(message.video_note.file_id)
        data['file_msg_id'].append(message.message_id)
        await state.update_data(file_msg_id=data['file_msg_id'], file_id=data['file_id'])
    elif message.document:
        if message.document.file_name.split('.')[-1] in ['m4a', 'm4b', 'm4p', 'm4r', 'mp3', 'aac', 'ac3', 'wav',
                                                         'alac', 'flac', 'flv', 'wma', 'amr', 'mpga', 'ogg', 'oga',
                                                         'mogg', '8svx', 'aif', 'ape', 'au', 'dss', 'opus', 'qcp',
                                                         'tta', 'voc', 'wv', 'm4p', 'm4v', 'webm', 'mts', 'm2ts', 'ts',
                                                         'mov', 'mp2', 'mxf', 'mp4', 'MP3']:
            logger.info(
                f'Get Document | ID --> {message.from_user.id}')
            file = await bot.get_file(message.document.file_id,
                                      request_timeout=300)
            audio_file_path = file.file_path.replace('\\', '/')
            duration, status = await get_duration_document(audio_file_path)
            os.remove(audio_file_path)
            if status is False:
                await message.answer(
                    text='🫢 Упс, с файлом что-то не то, обратитесь в поддержку, будем рады помочь /start')
                await create_error_db(message.from_user.id,
                                      'get_duration_document', 'get_audio', str(duration), session_maker)
                return
            data['file_id'].append(message.document.file_id)
            data['file_msg_id'].append(message.message_id)
            await state.update_data(file_msg_id=data['file_msg_id'], file_id=data['file_id'])
        else:
            await message.answer(
                text="⚠️ Похоже, этот формат файла <b>не поддерживается</b>. Попробуйте загрузить другой файл, и мы обязательно справимся!",
                reply_markup=await cancel_kb()
            )
            await state.set_state(FSMStart.start)
            return
    elif message.text:
        if 'http' in message.text:
            if 'google' in message.text:
                logger.info('Get google file | ID --> ' + str(message.from_user.id))
                file_path = await get_google_file(message.from_user.id, message.text)
            elif 'yandex' in message.text:
                logger.info('Get yandex file | ID --> ' + str(message.from_user.id))
                file_path = await get_yandex_file(message.from_user.id, message.text)
            elif 'rutube' in message.text:
                logger.info('Get rutube file | ID --> ' + str(message.from_user.id))
                file_path = await get_rutube_file(message.from_user.id, message.text)
            else:
                logger.info('Get youtube file | ID --> ' + str(message.from_user.id))
                file_path = await get_youtube_file(message.from_user.id, message.text)
            if file_path is None:
                await message.answer(
                    text='😅 Ошибка при обработке ссылки. Попробуйте ещё раз!',
                )
                await state.set_state(FSMStart.start)
                return
            logger.info('End download url | ID --> ' + str(message.from_user.id))
            duration, status = await get_duration_document(file_path)
            if status is False:
                await message.answer(
                    text='🫢 Упс, с файлом что-то не то, обратитесь в поддержку, будем рады помочь /start')
                await create_error_db(message.from_user.id,
                                      'get_url', 'get_audio', str(duration), session_maker)
                return
            data['url_files'].append(file_path)
            data['url_msg_id'].append(message.message_id)
            await state.update_data(url_msg_id=data['url_msg_id'], url_files=data['url_files'])
        else:
            await message.answer(
                text='😅 Похоже, вы неправильно ввели адрес ссылки. Попробуйте ещё раз!',
            )
            await state.set_state(FSMStart.start)
            return
    else:
        logger.info(
            f'Get voice | ID --> {message.from_user.id}')
        duration = message.voice.duration
        data['file_id'].append(message.voice.file_id)
        data['file_msg_id'].append(message.message_id)
        await state.update_data(file_msg_id=data['file_msg_id'], file_id=data['file_id'])

    await state.update_data(duration=data['duration'] + duration)

    data = await state.get_data()
    if (len(data['file_id']) + len(data["url_files"])) > 1:
        text = f'Вы загрузили <code>{len(data["file_id"]) + len(data["url_files"])}</code> файлов/ссылок'
    else:
        text = 'Вы загрузили <code>1</code> файл/ссылку'
    try:
        await data['msg'].delete()
    except Exception:
        pass
    msg = await message.answer_photo(
        photo=Configuration.second_photo_url,
        caption=f"⏱️ Ваш запрос\n"
                f"{text}\n\n"
                f"Необходимое время: <code>{await seconds_to_hms(int(data['duration']))}</code>.\n"
                "⏳ Время обработки займет <b>5-10 минут</b>. Спасибо за ваше терпение, мы ценим это! 💖\n\n"
                '<b>ШАГ 2: Настройка транскрибации</b>\n'
                '🔹 По умолчанию переводим всё видео/аудио в текст.\n'
                '🔹 Можно выбрать дополнительные настройки и форматы обработки.',
        reply_markup=await decoding_menu_kb()
    )
    await state.update_data(msg=msg)


async def get_audio_call_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if len(data['file_id']) > 1:
        text = f'Вы загрузили <code>{len(data["file_id"])}</code> файлов'
    else:
        text = 'Вы загрузили <code>1</code> файл'
    try:
        await data['msg'].delete()
    except Exception:
        pass
    msg = await call.message.answer_photo(
        photo=Configuration.second_photo_url,
        caption=f"⏱️ Ваш запрос\n"
                f"{text}\n\n"
                f"Необходимое время: <code>{await seconds_to_hms(int(data['duration']))}</code>.\n"
                "⏳ Время обработки займет <b>5-10 минут</b>. Спасибо за ваше терпение, мы ценим это! 💖\n\n"
                '<b>ШАГ 2: Настройка транскрибации</b>\n'
                '🔹 По умолчанию переводим всё видео/аудио в текст.\n'
                '🔹 Можно выбрать дополнительные настройки и форматы обработки.',
        reply_markup=await decoding_menu_kb()
    )
    await state.update_data(msg=msg)


async def get_more_audio(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMStart.start)
    await call.message.answer(
        text='<b>Отправьте ещё 1 файл/ссылку</b>',
        reply_markup=await cancel_kb()
    )


async def other_options(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['count_speakers'] == '':
        count_speakers = 'Автоопределение'
    else:
        count_speakers = data['count_speakers']
    if data['special_words'] == '':
        special_words = 'Нет'
    else:
        special_words = data['special_words']
    summary = str(data["format_summary"]).replace("[", "").replace("]", "").replace("'", "")
    try:
        msg = await data['msg'].edit_text(
            text='<b>Настройки по умолчанию:</b>\n'
                 f'- 👥 Количество спикеров: <b>{count_speakers}</b>\n'
                 f'- 📝 Специальные слова: <b>{special_words}</b>\n'
                 f'- 🎙️ Формат расшифровки: <b>{summary}</b>\n\n'
                 '✏️ Чтобы изменить настройки, выберите нужный параметр:',
            reply_markup=await other_settings_kb()
        )
    except Exception:
        try:
            await data['msg'].delete()
        except Exception:
            pass
        msg = await call.message.answer(
            text='<b>Настройки по умолчанию:</b>\n'
                 f'- 👥 Количество спикеров: <b>{count_speakers}</b>\n'
                 f'- 📝 Специальные слова: <b>{special_words}</b>\n'
                 f'- 🎙️ Формат расшифровки: <b>{summary}</b>\n\n'
                 '✏️ Чтобы изменить настройки, выберите нужный параметр:',
            reply_markup=await other_settings_kb()
        )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.message.register(get_audio, FSMStart.start, F.content_type.in_(
        {'document', 'audio', 'video', 'voice', 'video_note', 'text'}), ~F.text.startswith('/'))
    dp.callback_query.register(get_audio_call_data, F.data == 'settings')
    dp.callback_query.register(get_more_audio, F.data == 'more_audio')
    dp.callback_query.register(other_options, F.data == 'other_options')
