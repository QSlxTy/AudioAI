from mutagen import File
from pydub import AudioSegment
from moviepy import  *
from bot_start import bot, logger


async def get_duration_document(path):
    try:
        logger.info(f'Get get duration {path}')
        if path.split('.')[-1] in ['webm']:
            audio = AudioSegment.from_file(path)
            logger.info(f'Webm type get duration {audio}')
            return audio.duration_seconds, True
        elif path.split('.')[-1] in ['mp4']:
            video = VideoFileClip(path)
            logger.info(f'Video type get duration {video}')

            return video.duration, True
        else:
            audio = File(path)
            logger.info(f'Media type get duration {audio}')
            return audio.info.length, True
    except Exception as _ex:
        logger.exception(f'get_duration_document --> {_ex}')
        return _ex, False


async def seconds_to_hms(seconds):
    try:
        seconds = int(seconds)

        if seconds < 10:  # Если не хватает на 10 секунд
            return "0 сек"

        minutes = seconds // 60
        sec = seconds % 60

        if minutes < 1:  # Если не хватает на 1 минуту
            return f"{sec} сек"

        # Форматируем минуты с разделителем, если больше 1000
        if minutes >= 1000:
            minutes_str = f"{minutes // 1000} {minutes % 1000:03d}"
        else:
            minutes_str = str(minutes)

        return f"{minutes_str} мин {sec} сек"

    except ValueError:
        return "Некорректное значение"


async def split_message(message: str) -> list:
    return [message[i:i + 4000] for i in range(0, len(message), 4000)]


languages = [
    "ru",
    "es",
    "fr",
    "de",
    "zh",
    "ja",
    "pt",
    "it",
    "ko",
    "ar",
    "hi",
    "bn",
    "pa",
    "jv",
    "vi",
    "te",
    "mr",
    "ta",
    "tr",
    "fa"
]


async def download_file(file_id: str, destination: str) -> None:
    # Получаем файл
    file = await bot.get_file(file_id)
    file.download(destination)
