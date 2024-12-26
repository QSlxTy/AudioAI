import os
from uuid import uuid4

import aioboto3

from bot_start import logger
from src.config import BotConfig


async def upload_photo_to_yandex_s3(file_path, folder: str = "photos_georgy_MJ"
                                    ) -> str:
    """
    Асинхронно загружает фотографию на Yandex S3 и возвращает публичный URL.
    :param file_path: Путь к файлу
    :param folder: Папка в бакете S3 для хранения фото.
    :return: Публичный URL загруженной фотографии на Yandex S3.
    """
    try:

        # Генерируем уникальное имя для файла

        file_extension = os.path.splitext(file_path)[1]
        unique_filename = f"{folder}/{uuid4()}{file_extension}"

        # Создаём сессию aioboto3
        session = aioboto3.Session()
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
            file.close()
        async with session.resource(
                "s3",
                endpoint_url='https://storage.yandexcloud.net/',
                aws_access_key_id=BotConfig.yandex_access_key,
                aws_secret_access_key=BotConfig.yandex_secret_key,
                region_name=BotConfig.yandex_region,
        ) as s3_resource:
            obj = await s3_resource.Object(BotConfig.yandex_bucket_name, unique_filename)
            await obj.put(
                Body=file_bytes,
                ContentType=f"image/{file_extension.lstrip('.')}",
                ACL="public-read",
            )

        # Формируем URL
        s3_url = f"https://storage.yandexcloud.net/{BotConfig.yandex_bucket_name}/{unique_filename}"

        return s3_url

    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке файла на Yandex S3: {e}")
        raise


async def delete_photo_from_yandex_s3(file_path: str) -> bool:
    """
    Асинхронно удаляет фотографию из Yandex S3.
    :param file_path: Путь к файлу в бакете S3.
    :return: True, если файл успешно удален, иначе False.
    """
    try:
        # Создаём сессию aioboto3
        session = aioboto3.Session()

        async with session.resource(
                "s3",
                endpoint_url='https://storage.yandexcloud.net/',
                aws_access_key_id=BotConfig.yandex_access_key,
                aws_secret_access_key=BotConfig.yandex_secret_key,
                region_name=BotConfig.yandex_region,
        ) as s3_resource:
            obj = await s3_resource.Object(BotConfig.yandex_bucket_name, file_path)
            await obj.delete()

        logger.info(f"Файл {file_path} успешно удален из Yandex S3.")
        return True

    except Exception as e:
        logger.error(f"Ошибка при удалении файла {file_path} из Yandex S3: {e}")
        return False
