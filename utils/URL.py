import os

import yadisk
from pydub import AudioSegment

from bot_start import logger
from src.config import Configuration
from utils.replicate_api import replicate_func_url

yandex = yadisk.YaDisk(token=Configuration.yadisk_token)


async def upload_file(file_path, yandex_path):
    logger.info(f"Start upload file to drop box")
    with open(file_path, 'rb'):
        yandex.upload(file_path, yandex_path)
    logger.info(f"File {file_path} uploaded to {yandex_path}")


async def create_shared_link(yandex_path):
    url = yandex.get_download_link(yandex_path)
    logger.info(f'link created {url}')

    return url


async def delete_file(yandex_path):
    try:
        yandex.remove(yandex_path)
        logger.info(f"File --> {yandex_path} deleted")
    except Exception as _ex:
        logger.error(f"Error delete file --> {_ex}")


async def upload_yadisk_file(local_file_path, lang, speakers, words, format_decoding, user_id,
                             session_maker):
    try:
        audio = AudioSegment.from_file(local_file_path)
        local_file_path_new = local_file_path + '_new.mp3'
        audio.export(local_file_path_new, format="mp3")
        os.remove(local_file_path)
        await upload_file(local_file_path_new, f'/{user_id}_file.mp3')
        link = await create_shared_link(f'/{user_id}_file.mp3')
        decode_path = await replicate_func_url(link, lang, speakers, words, format_decoding, user_id, session_maker)
        await delete_file(f'/{user_id}_file.mp3')
        return local_file_path_new, decode_path
    except Exception as _ex:
        logger.error(f'Decoding error {_ex}')
        return False
