from handlers.user import start, tariff_handler, get_audio, decoding_audio, support, buy_balance, promocode_menu
from handlers.user.decoding_settings import choose_decoding, choose_lang, choose_speakers, choose_summary, choose_words


def register_user_handler(dp):
    start.register_start_handler(dp)
    tariff_handler.register_handler(dp)
    get_audio.register_handler(dp)
    choose_words.register_handler(dp)
    choose_speakers.register_handler(dp)
    choose_lang.register_handler(dp)
    choose_decoding.register_handler(dp)
    choose_summary.register_handler(dp)
    decoding_audio.register_handler(dp)
    support.register_handler(dp)
    buy_balance.register_handler(dp)
    promocode_menu.register_handler(dp)
