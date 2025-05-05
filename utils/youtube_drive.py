import asyncio
import os
from datetime import datetime

import yt_dlp

from bot_start import logger


async def get_youtube_file(user_id, url):
    try:
        user_directory = f'media/{user_id}/'
        os.makedirs(user_directory, exist_ok=True)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Настройки для yt-dlp
        ydl_opts = {
            'format': 'worstaudio',  # Извлечение лучшего доступного аудио
            'quiet': True,
            'noplaylist': True,
            'outtmpl': f'media/{user_id}/{current_time}',
            'postprocessors':
                [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ],
        }

        await asyncio.get_running_loop().run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))

        return f'media/{user_id}/{current_time}.mp3'
    except Exception as _ex:
        logger.error('Error in get_youtube_file --> ' + str(_ex))
