import os

from pydub import AudioSegment

from bot_start import logger
from utils.replicate_api import replicate_func_url
from utils.s3 import upload_photo_to_yandex_s3, delete_photo_from_yandex_s3


async def upload_yadisk_file(file_id, local_file_path, lang, speakers, words, format_decoding, user_id, session_maker):

    if 'mp3' in local_file_path or 'MP3' in local_file_path:
        bucket_url = await upload_photo_to_yandex_s3(local_file_path)
        os.remove(local_file_path)
    else:
        audio = AudioSegment.from_file(local_file_path)
        local_file_path_new = f'media/{user_id}/' + file_id + '_new.mp3'
        audio.export(local_file_path_new, format="mp3")
        os.remove(local_file_path)
        bucket_url = await upload_photo_to_yandex_s3(local_file_path_new)
        os.remove(local_file_path_new)

    logger.info(f'End upload bucket --> {user_id}')
    logger.info(f'Start replicate --> {user_id}')
    decode_path = await replicate_func_url(
        bucket_url, lang, speakers, words, format_decoding, user_id,
        session_maker
    )
    await delete_photo_from_yandex_s3(
        bucket_url.split('https://storage.yandexcloud.net/chatbotgigacht')[-1][1:]
    )
    return decode_path
