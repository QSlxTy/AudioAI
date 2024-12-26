import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from bot_start import bot
from keyboards.user.user_keyboard import settings_audio_kb, cancel_kb
from utils.aiogram_helper import seconds_to_hms, get_duration_document
from utils.states.user import FSMStart


async def get_audio(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if not os.path.exists(f'media/{message.from_user.id}'):
        os.makedirs(f'media/{message.from_user.id}')
    await message.answer(
        text='<b>Начал скачивание файла</b>'
    )
    if message.video:
        file = await bot.get_file(file_id=message.video.file_id, request_timeout=False)
        duration = message.video.duration
        data['path'].append(file.file_path.replace('\\', '/'))
        await state.update_data(path=data['path'], file_id=message.video.file_id)

    elif message.audio:
        file = await bot.get_file(message.audio.file_id, request_timeout=False)
        duration = message.audio.duration
        data['path'].append(file.file_path.replace('\\', '/'))
        await state.update_data(path=data['path'], file_id=message.audio.file_id)

    elif message.video_note:
        file = await bot.get_file(file_id=message.video_note.file_id, request_timeout=False)
        duration = message.video_note.duration
        data['path'].append(file.file_path.replace('\\', '/'))
        await state.update_data(path=data['path'], file_id=message.video_note.file_id)
    elif message.document:
        file = await bot.get_file(file_id=message.document.file_id, request_timeout=False)
        duration = await get_duration_document(file.file_path.replace('\\', '/'))
        data['path'].append(file.file_path.replace('\\', '/'))
        await state.update_data(path=data['path'], file_id=message.document.file_id)

    else:
        file = await bot.get_file(file_id=message.voice.file_id, request_timeout=False)
        duration = message.voice.duration
        data['path'].append(file.file_path.replace('\\', '/'))
        await state.update_data(path=data['path'], file_id=message.voice.file_id)

    await state.update_data(duration=data['duration'] + duration)
    data = await state.get_data()

    if data['lang'] == '':
        lang = 'Автоопределение'
    else:
        lang = data['lang']
    if data['count_speakers'] == '':
        count_speakers = 'Автоопределение'
    else:
        count_speakers = data['count_speakers']
    if data['special_words'] == '':
        special_words = 'Нет'
    else:
        special_words = data['special_words']

    if len(data['path']) > 1:
        text = f'Длина ваших <code>{len(data["path"])}</code> файлов'
    else:
        text = 'Ваш файл длится'
    await message.answer(
        text=f'<b>{text} - <code>{await seconds_to_hms(int(data["duration"]))}</code>\n'
             f'С вас спишем - <code>{await seconds_to_hms(int(data["duration"]))}</code>\n'
             f'Время обработки - <code>5-10</code> минут.\n\n'
             f'Дополнительные настройки:\n'
             f'·Язык - <code>{lang}</code>\n'
             f'·Кол-во спикеров - <code>{count_speakers}</code>\n'
             f'·Специальные слова - <code>{special_words}</code>\n'
             f'·Формат расшифровки - <code>{data["format_decoding"]}</code>\n'
             f'·Формат саммари - <code>{data["format_summary"]}</code>\n\n'
             f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
        reply_markup=await settings_audio_kb()
    )
    data['file_msg_id'].append(message.message_id)
    await state.update_data(duration_sec=duration, file_msg_id=data['file_msg_id'])


async def get_audio_call_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data['lang'] == '':
        lang = 'Автоопределение'
    else:
        lang = data['lang']
    if data['count_speakers'] == '':
        count_speakers = 'Автоопределение'
    else:
        count_speakers = data['count_speakers']
    if data['special_words'] == '':
        special_words = 'Нет'
    else:
        special_words = data['special_words']
    if len(data['path']) > 1:
        text = f'Длина ваших <code>{len(data["path"])}</code> файлов'
    else:
        text = 'Ваш файл длится'
    await call.message.answer(
        text=f'<b>{text} - <code>{await seconds_to_hms(int(data["duration"]))}</code>\n'
             f'С вас спишем - <code>{await seconds_to_hms(int(data["duration_sec"]))}</code>\n'
             f'Время обработки - <code>5-10</code> минут.\n\n'
             f'Дополнительные настройки:\n'
             f'·Язык - <code>{lang}</code>\n'
             f'·Кол-во спикеров - <code>{count_speakers}</code>\n'
             f'·Специальные слова - <code>{special_words}</code>\n'
             f'·Формат расшифровки - <code>{data["format_decoding"]}</code>\n'
             f'·Формат саммари - <code>{data["format_summary"]}</code>\n\n'
             f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
        reply_markup=await settings_audio_kb()
    )


async def get_more_audio(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMStart.start)
    await call.message.answer(
        text='<b>Отправьте ещё 1 файл</b>',
        reply_markup=await cancel_kb()
    )


def register_handler(dp: Dispatcher):
    dp.message.register(get_audio, FSMStart.start, F.content_type.in_(
        {'document', 'audio', 'video', 'voice', 'video_note'}))
    dp.callback_query.register(get_audio_call_data, F.data == 'settings')
    dp.callback_query.register(get_more_audio, F.data == 'more_audio')
