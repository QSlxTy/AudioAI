from pydub import AudioSegment

from bot_start import bot


async def get_duration_document(path):
    audio = AudioSegment.from_file(path)
    return audio.duration_seconds


async def seconds_to_hms(seconds):
    try:
        minutes = int(seconds) // 60
        sec = int(seconds) % 60
        return f"{int(minutes)}мин {int(sec)}сек"
    except ValueError:
        return f"1 сек"


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
