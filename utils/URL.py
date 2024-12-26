import os

from pydub import AudioSegment

from utils.replicate_api import replicate_func_url
from utils.s3 import upload_photo_to_yandex_s3, delete_photo_from_yandex_s3


async def upload_yadisk_file(bot, file_id, local_file_path, lang, speakers, words, format_decoding, user_id,
                             session_maker):
    # try:
    audio = AudioSegment.from_file(local_file_path)
    print(audio)
    local_file_path_new = f'media/{user_id}/' + file_id + '_new.mp3'
    print(local_file_path_new)
    audio.export(local_file_path_new, format="mp3")
    os.remove(local_file_path)
    bucket_url = await upload_photo_to_yandex_s3(local_file_path_new
    )
    print(bucket_url)
    decode_path = await replicate_func_url(bucket_url, lang, speakers, words, format_decoding, user_id,
                                           session_maker)
    os.remove(local_file_path_new)
    await delete_photo_from_yandex_s3(bucket_url.split('https://storage.yandexcloud.net/chatbotgigacht')[-1][1:])
    return decode_path
    # except Exception as _ex:
    #     logger.error(f'Decoding error {_ex}')
    #     return False, False
