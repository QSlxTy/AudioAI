from pydub import AudioSegment


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
    ["ru", "en"],
    ["es", "en"],
    ["fr", "en"],
    ["de", "en"],
    ["zh", "en"],
    ["ja", "en"],
    ["pt", "en"],
    ["it", "en"],
    ["ko", "en"],
    ["ar", "en"],
    ["hi", "en"],
    ["bn", "en"],
    ["pa", "en"],
    ["jv", "en"],
    ["vi", "en"],
    ["te", "en"],
    ["mr", "en"],
    ["ta", "en"],
    ["tr", "en"],
    ["fa", "en"]
]