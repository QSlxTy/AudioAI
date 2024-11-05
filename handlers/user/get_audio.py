import os

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot_start import bot, logger
from keyboards.user.user_keyboard import settings_audio_kb, settings_other_audio_kb
from src.config import UserBotConfig
from telethon_api.user_bot import get_info_file, get_big_data, get_message_info
from utils.aiogram_helper import seconds_to_hms, get_duration_document
from utils.states.user import FSMStart


async def get_audio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        lang = data['lang']
    except KeyError:
        await state.update_data(lang='')
    try:
        speakers = data['count_speakers']
    except KeyError:
        await state.update_data(count_speakers='')
    try:
        special_words = data['special_words']
    except KeyError:
        await state.update_data(special_words='')
    try:
        format_decode = data['format_decoding']
    except KeyError:
        await state.update_data(format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров')
    try:
        format_summary = data['format_summary']
    except KeyError:
        await state.update_data(format_summary='Протокол встречи')
    if not os.path.exists(f'media/{message.from_user.id}'):
        os.makedirs(f'media/{message.from_user.id}')
    try:
        if message.video:
            await bot.download(message.video,
                               destination=f'media/{message.from_user.id}/{message.video.file_id}_video.mp4')
            duration = message.video.duration
            await state.update_data(path=f'media/{message.from_user.id}/{message.video.file_id}_video.mp4')
        elif message.audio:
            await bot.download(message.audio,
                               destination=f'media/{message.from_user.id}/{message.audio.file_id}_audio.mp3')
            duration = message.audio.duration
            await state.update_data(path=f'media/{message.from_user.id}/{message.audio.file_id}_audio.mp3')
        elif message.video_note:
            await bot.download(message.video_note,
                               destination=f'media/{message.from_user.id}/{message.video_note.file_id}_videonote.mp4')
            duration = message.video_note.duration
            await state.update_data(
                path=f'media/{message.from_user.id}/{message.video_note.file_id}_videonote.mp3')
        elif message.document:
            await state.update_data(
                path=f'media/{message.from_user.id}/{message.document.file_id}_document.mp3')
            duration = await get_duration_document(
                f'media/{message.from_user.id}/{message.document.file_id}_document.mp3')
        else:
            await bot.download(message.voice,
                               destination=f'media/{message.from_user.id}/{message.voice.file_id}_voice.mp3')
            duration = message.voice.duration
            await state.update_data(path=f'media/{message.from_user.id}/{message.voice.file_id}_voice.mp3')
        data = await state.get_data()
        await state.update_data(duration=duration)
        await data['msg'].delete()
        msg = await message.answer(
            text=f'<b>Ваш файл длится - <code>{await seconds_to_hms(int(duration))}</code>\n'
                 f'С вас спишем - <code>{await seconds_to_hms(int(duration))}</code>\n'
                 f'Время обработки - 5-10 минут.\n\n'
                 f'Дополнительные настройки:\n'
                 f'·Язык - <code>Автоопределение</code>\n'
                 f'·Кол-во спикеров - <code>Автоопределение</code>\n'
                 f'·Специальные слова - <code>Нет</code>\n'
                 f'·Формат расшифровки - <code>Расшифровка с тайм-кодами и разбиением на спикеров</code>\n'
                 f'·Формат саммари - <code>Протокол встречи</code>\n\n'
                 f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
            reply_markup=await settings_audio_kb()
        )
        await state.update_data(duration_sec=duration, msg=msg)
    except Exception as _ex:
        logger.info(f'Get big data --> {_ex}')
        await bot.forward_message(chat_id=UserBotConfig.telegram_id, from_chat_id=message.chat.id,
                                  message_id=message.message_id)
        message_info = await get_message_info()
        data = await state.get_data()
        try:
            duration, size = await get_info_file(message_info)
            await data['msg'].delete()
            msg = await message.answer(
                text=f'<b>Ваш файл длится - <code>{await seconds_to_hms(int(duration))}</code>\n'
                     f'С вас спишем - <code>{await seconds_to_hms(int(duration))}</code>\n'
                     f'Время обработки - 5-10 минут.\n\n'
                     f'Дополнительные настройки:\n'
                     f'·Язык - <code>Автоопределение</code>\n'
                     f'·Кол-во спикеров - <code>Автоопределение</code>\n'
                     f'·Специальные слова - <code>Нет</code>\n'
                     f'·Формат расшифровки - <code>Расшифровка с тайм-кодами и разбиением на спикеров</code>\n'
                     f'·Формат саммари - <code>Протокол встречи</code>\n\n'
                     f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
                reply_markup=await settings_audio_kb()
            )
            await state.update_data(msg=msg, duration_sec=duration, size=size, count_speakers='', lang='',
                                    special_words='',
                                    format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров',
                                    format_summary='Протокол встречи')
        except AttributeError:
            await data['msg'].delete()
            msg = await message.answer(text='<b>Файл оказался большой, начинаю загрузку на сервер...</b>')
            await bot.forward_message(chat_id=UserBotConfig.telegram_id, from_chat_id=message.chat.id,
                                      message_id=message.message_id)
            path, duration, size = await get_big_data(message.from_user.id, msg.message_id)

            msg = await bot.send_message(chat_id=message.from_user.id,
                                         text=f'<b>Ваш файл длится - <code>{await seconds_to_hms(int(duration))}</code>\n'
                                              f'С вас спишем - <code>{await seconds_to_hms(int(duration))}</code>\n'
                                              f'Время обработки - 5-10 минут.\n\n'
                                              f'Дополнительные настройки:\n'
                                              f'·Язык - <code>Автоопределение</code>\n'
                                              f'·Кол-во спикеров - <code>Автоопределение</code>\n'
                                              f'·Специальные слова - <code>Нет</code>\n'
                                              f'·Формат расшифровки - <code>Расшифровка с тайм-кодами и разбиением на спикеров</code>\n'
                                              f'·Формат саммари - <code>Протокол встречи</code>\n\n'
                                              f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
                                         reply_markup=await settings_other_audio_kb()
                                         )
            await state.update_data(path=path, duration_sec=duration, size=size, msg=msg)


async def get_audio_call_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        lang = data['lang']
    except KeyError:
        lang = 'Автоопределение'
        await state.update_data(lang='')
    try:
        speakers = data['count_speakers']
    except KeyError:
        speakers = 'Автоопределение'
        await state.update_data(count_speakers='')
    try:
        special_words = data['special_words']
    except KeyError:
        special_words = 'Нет'
        await state.update_data(special_words='')
    try:
        format_decode = data['format_decoding']
    except KeyError:
        format_decode = 'Расшифровка с тайм-кодами и разбиением на спикеров'
        await state.update_data(format_decoding='Расшифровка с тайм-кодами и разбиением на спикеров')
    try:
        format_summary = data['format_summary']
    except KeyError:
        format_summary = 'Протокол встречи'
        await state.update_data(format_summary='Протокол встречи')
    try:
        msg = await data['msg'].edit_text(
            text=f'<b>Ваш файл длится - <code>{await seconds_to_hms(int(data["duration_sec"]))}</code>.\n'
                 f'С вас спишем - <code>{await seconds_to_hms(int(data["duration_sec"]))}</code>\n'
                 f'Время обработки - 5-10 минут.\n\n'
                 f'Дополнительные настройки:\n'
                 f'·Язык - <code>{lang}</code>\n'
                 f'·Кол-во спикеров - <code>{speakers}</code>\n'
                 f'·Специальные слова - <code>{special_words}</code>\n'
                 f'·Формат расшифровки - <code>{format_decode}</code>\n'
                 f'·Формат саммари - <code>{format_summary}</code>\n\n'
                 f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
            reply_markup=await settings_audio_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text=f'<b>Ваш файл длится - <code>{await seconds_to_hms(int(data["duration_sec"]))}</code>\n'
                 f'С вас спишем - <code>{await seconds_to_hms(int(data["duration_sec"]))}</code>\n'
                 f'Время обработки - 5-10 минут.\n\n'
                 f'Дополнительные настройки:\n'
                 f'·Язык - <code>{lang}</code>\n'
                 f'·Кол-во спикеров - <code>{speakers}</code>\n'
                 f'·Специальные слова - <code>[{special_words}]</code>\n'
                 f'·Формат расшифровки - <code>{format_decode}</code>\n'
                 f'·Формат саммари - <code>{format_summary}</code>\n\n'
                 f'Чтобы изменить дополнительные настройки, нажмите на кнопки ниже и добавьте нужные данные</b>',
            reply_markup=await settings_audio_kb()
        )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.message.register(get_audio, FSMStart.start, F.content_type.in_(
        {'document', 'audio', 'video', 'voice', 'video_note'}))
    dp.callback_query.register(get_audio_call_data, F.data == 'settings')
