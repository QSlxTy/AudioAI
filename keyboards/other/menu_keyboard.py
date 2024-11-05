from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Тарифы·', callback_data='check_tariff')
    builder.button(text='·Поддержка·', callback_data='support')
    builder.adjust(1, 2)
    return builder.as_markup()
