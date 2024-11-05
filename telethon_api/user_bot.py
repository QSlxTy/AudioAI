import logging
import time

from telethon.errors import AuthKeyDuplicatedError, PhoneNumberBannedError, UserDeactivatedBanError

from bot_start import client, bot
from src.config import UserBotConfig
from utils.aiogram_helper import get_duration_document


async def get_big_data(user_id, msg_id):
    try:
        message = await client.get_messages(UserBotConfig.bot_username, limit=1)
        start_time = time.time()
        logging.info('Start download')
        file_path = await client.download_media(message[0].media, file=f'media/{user_id}',
                                                progress_callback=lambda current, total: progress(current, total,
                                                                                                  user_id, msg_id))
        end_time = time.time()
        download_time = end_time - start_time
        file_path = file_path.split('/')[1]
        file_path = f'media/' + file_path
        file_path = file_path.replace("\\", '/')
        logging.info(f'Success download, time --> {round(download_time, 2)}, file saved to --> {file_path}')
        try:
            duration = message[0].media.document.attributes[0].duration
        except AttributeError:
            duration = await get_duration_document(file_path)
        size = message[0].media.document.size

        return file_path, duration, size
    except (AuthKeyDuplicatedError, PhoneNumberBannedError, ConnectionError, UserDeactivatedBanError) as _ex:
        logging.error(f'Telethon ERROR --> {_ex}')

async def get_message_info():
    message = await client.get_messages(UserBotConfig.bot_username, limit=1)
    return message


async def get_info_file(message):
    duration = message[0].media.document.attributes[0].duration
    size = message[0].media.document.size
    logging.info(f'Duration --> {duration} sec Size  --> {size} b')
    return duration, size


async def progress(current, total, user_id, msg_id):
    if int(current * 100 / total) % 3 == 0:
        await bot.edit_message_text(chat_id=user_id,
                                    text=f"<b>Статус загрузки файла: </b><code>{current * 100 / total:.1f}</code> %",
                                    message_id=msg_id)

    if f'{current * 100 / total:.1f}' == '100.0':
        await bot.edit_message_text(chat_id=user_id,
                                    text=f"<b>Завершено <code>100%</code></b>",
                                    message_id=msg_id)

