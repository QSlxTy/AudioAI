import os
from datetime import datetime
import requests

from bot_start import logger


async def get_yandex_file(user_id, public_url):
    base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
    params = {"public_key": public_url}

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        logger.error(f"Ошибка при получении ссылки: {response.status_code}, {response.text}")
        return None

    download_url = response.json().get("href")
    if not download_url:
        logger.error("Не удалось получить прямую ссылку для скачивания.")
        return None

    user_folder = f"media/{user_id}"
    os.makedirs(user_folder, exist_ok=True)
    head_resp = requests.head(download_url)
    content_type = head_resp.headers.get('Content-Type', '')
    extension = ''
    if 'audio' in content_type:
        extension = '.mp3'
    elif 'image' in content_type:
        extension = '.jpg'
    elif 'video' in content_type:
        extension = '.mp4'

    filename = f"{user_folder}/yandex_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}{extension}"
    logger.info(f'Get yandex MIME --> {extension}')
    with requests.get(download_url, stream=True) as r:
        if r.status_code != 200:
            logger.error(f"Ошибка при скачивании файла: {r.status_code}, {r.text}")
            return None
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return filename
