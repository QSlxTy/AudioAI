import io
import os
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials

from bot_start import logger


async def get_extension(mime_type):
    mime_types = {
        'application/pdf': '.pdf',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'audio/mpeg': '.mp3',
        'video/mp4': '.mp4',
    }
    return mime_types.get(mime_type, '')


async def get_google_file(user_id, url):
    try:
        service_account_file = 'utils/praxis-road-437208-v7-2883f49f03fa.json'
        file_id = url.split('/d/')[1].split('/')[0]
        logger.info('Get Google ID --> ' + str(file_id))

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/drive.readonly'],
        )

        service = build('drive', 'v3', credentials=credentials)

        file_metadata = service.files().get(fileId=file_id).execute()

        mime_type = file_metadata.get('mimeType')
        logger.info('Google mimeType --> ' + mime_type)
        extension = await get_extension(mime_type)

        request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(f'Download {int(status.progress() * 100)}%.')

        directory_path = f"media/{user_id}/"
        os.makedirs(directory_path, exist_ok=True)

        file_path = f"{directory_path}google_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}{extension}"

        with open(file_path, 'wb') as f:
            f.write(fh.getvalue())

        return file_path

    except Exception as ex:
        logger.error(f"Google Drive error: {ex}")
        return None
