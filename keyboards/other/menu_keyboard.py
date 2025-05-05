from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu_kb(is_admin):
    builder = InlineKeyboardBuilder()
    builder.button(text='🔘 Тарифы', callback_data='check_tariff')
    builder.button(text='🔘 Сделать транскрибацию', callback_data='first_step')
    builder.button(text='🔘 Поддержка', callback_data='support')
    if is_admin is True:
        builder.button(text='➖➖➖➖➖➖➖', callback_data='empty')
        builder.button(text='💬 Меню рассылки', callback_data='mail')

    builder.adjust(1)
    return builder.as_markup()


async def decoding_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Дополнительные настройки', callback_data='other_options')
    builder.button(text='Загрузить ещё файл', callback_data='more_audio')
    builder.button(text='🟢 ЗАПУСТИТЬ ТРАНСКРИБАЦИЮ', callback_data='go_decoding')
    builder.adjust(1)
    return builder.as_markup()


async def other_settings_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔘 Выбрать количество спикеров', callback_data='count_speakers')
    builder.button(text='🔘 Добавить специальные слова', callback_data='add_word')
    builder.button(text='🔘 Выбрать форматы обработки ', callback_data='format_summary')
    builder.button(text='🟢 ЗАПУСТИТЬ ТРАНСКРИБАЦИЮ', callback_data='go_decoding')
    builder.button(text='🔘 Назад', callback_data='settings')
    builder.adjust(1)
    return builder.as_markup()
