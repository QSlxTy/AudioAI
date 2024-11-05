from aiogram.utils.keyboard import InlineKeyboardBuilder


async def back_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·В главное меню·', callback_data='main_menu')
    return builder.as_markup()


async def tariff_list_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·30 минут·', callback_data='choose_tariff:30')
    builder.button(text='·120 минут·', callback_data='choose_tariff:120')
    builder.button(text='·480 минут·', callback_data='choose_tariff:480')
    builder.button(text='·3000 минут·', callback_data='choose_tariff:3000')
    builder.button(text='·Использовать промокод·', callback_data='go_promo')
    builder.button(text='·В главное меню·', callback_data='main_menu')
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


async def back_tariff_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Назад·', callback_data='check_tariff')
    return builder.as_markup()


async def settings_audio_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Продолжить·', callback_data='go_decoding')
    builder.button(text='·Отменить·', callback_data='main_menu')
    builder.button(text='·Указать язык·', callback_data='choose_lang')
    builder.button(text='·Количество спикеров·', callback_data='count_speakers')
    builder.button(text='·Добавить слова·', callback_data='add_word')
    builder.adjust(2, 1, 1, 1, 1, 1)
    return builder.as_markup()


async def settings_other_audio_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Продолжить·', callback_data='go_other_decoding')
    builder.button(text='·Отменить·', callback_data='main_menu')
    builder.button(text='·Указать язык·', callback_data='choose_lang')
    builder.button(text='·Количество спикеров·', callback_data='count_speakers')
    builder.button(text='·Добавить слова·', callback_data='add_word')
    builder.adjust(2, 1, 1, 1, 1, 1)
    return builder.as_markup()


async def choose_lang_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Автоопределение·', callback_data='auto_lang')
    builder.button(text='·Назад·', callback_data='settings')
    builder.adjust(1)
    return builder.as_markup()


async def choose_speakers_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Автоопределение·', callback_data='auto_speakers')
    builder.button(text='·Назад·', callback_data='settings')
    builder.adjust(1)
    return builder.as_markup()


async def choose_decoding_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·1·', callback_data='choose_format_decode:1')
    builder.button(text='·2·', callback_data='choose_format_decode:2')
    builder.adjust(1)
    return builder.as_markup()


async def choose_summary_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Протокол встречи·', callback_data='choose_summary:1')
    builder.button(text='·Краткая выжимка·', callback_data='choose_summary:2')
    builder.button(text='·Анализ диалога·', callback_data='choose_summary:3')
    builder.button(text='·Перечень действий·', callback_data='choose_summary:4')
    builder.adjust(1)
    return builder.as_markup()


async def go_decode_settings_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Назад·', callback_data='settings')
    return builder.as_markup()


async def get_email_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Мне не нужен чек·', callback_data='no_check')
    builder.button(text='·В главное меню·', callback_data='main_menu')
    builder.adjust(1)
    return builder.as_markup()


async def accept_rules_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Подтвердить·', callback_data='accept_create')
    builder.button(text='·В главное меню·', callback_data='main_menu')
    builder.adjust(1)
    return builder.as_markup()


async def payment_link_kb(url, payment_id):
    builder = InlineKeyboardBuilder()
    if payment_id == 0:
        builder.button(text='·Ссылка·', url=url)
    builder.button(text='·Проверить оплату·', callback_data='check_payment')
    builder.adjust(1)
    return builder.as_markup()
