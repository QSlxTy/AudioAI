from aiogram.utils.keyboard import InlineKeyboardBuilder

from integrations.database.models.tariff import get_all_tariff_db


async def back_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·В главное меню·', callback_data='main_menu')
    return builder.as_markup()


async def cancel_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Отмена·', callback_data='main_menu')
    return builder.as_markup()


async def tariff_list_kb(session_maker):
    tariffs = await get_all_tariff_db(session_maker)
    builder = InlineKeyboardBuilder()
    for tariff in tariffs:
        builder.button(text=f'·{tariff.tariff_name} минут·', callback_data=f'choose_tariff:{tariff.tariff_name}')
    builder.button(text='·Использовать промокод·', callback_data='go_promo')
    builder.button(text='·В главное меню·', callback_data='main_menu')
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


async def back_tariff_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Назад·', callback_data='check_tariff')
    return builder.as_markup()



async def choose_words_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Автоопределение·', callback_data='auto_words')
    builder.button(text='·Вернуться в настройки·', callback_data='other_options')
    builder.adjust(1)
    return builder.as_markup()


async def choose_speakers_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Автоопределение·', callback_data='auto_speakers')
    builder.button(text='·Вернуться в настройки·', callback_data='other_options')
    builder.adjust(1)
    return builder.as_markup()



async def choose_summary_kb(list_summary):
    if 'Протокол встречи' in list_summary:
        text_summary_1 = 'Протокол встречи ✅ '
    else:
        text_summary_1 = 'Протокол встречи ❌'
    if 'Саммари' in list_summary:
        text_summary_2 = 'Саммари ✅ '
    else:
        text_summary_2 = 'Саммари ❌'
    if 'Перечень действий' in list_summary:
        text_summary_3 = 'Перечень действий ✅ '
    else:
        text_summary_3 = 'Перечень действий ❌'
    if 'Анализ диалога' in list_summary:
        text_summary_4 = 'Анализ диалога ✅ '
    else:
        text_summary_4 = 'Анализ диалога ❌'
    builder = InlineKeyboardBuilder()
    builder.button(text=text_summary_1, callback_data='choose_summary:1')
    builder.button(text=text_summary_2, callback_data='choose_summary:2')
    builder.button(text=text_summary_3, callback_data='choose_summary:3')
    builder.button(text=text_summary_4, callback_data='choose_summary:4')
    builder.button(text='·Вернуться в настройки·', callback_data='other_options')
    builder.adjust(1)
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


async def end_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·Сделать новую транскрибацию·', callback_data='first_step')
    return builder.as_markup()

async def go_decode_settings_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='·В настройки·', callback_data='other_settings')
    return builder.as_markup()

async def choose_mail_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='✔️ Подвердить', callback_data='go_mail:True')
    builder.button(text='❌ Отмена', callback_data='go_mail:False')
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()