from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import choose_lang_kb, go_decode_settings_kb
from utils.aiogram_helper import languages
from utils.states.user import FSMCreate


async def choose_lang(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_lang)
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Пожалуйста, укажите язык речи в формате "en", "ru" или нажмите <code>·Автоопределение·</code></b>',
            reply_markup=await choose_lang_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Пожалуйста, укажите язык речи в формате "en", "ru" или нажмите <code>·Автоопределение·</code></b>',
            reply_markup=await choose_lang_kb()
        )
    await state.update_data(msg=msg)


async def get_lang(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    if message.text not in languages:
        try:
            msg = await data['msg'].edit_text(
                text=f'<b>К сожалению вы ввели некорректное значение языка</b>\n\n'
                     f'Введите ещё раз ❗️\n\n'
                     f'Верный формат <code>ru, en, uk</code>',
                reply_markup=await go_decode_settings_kb()
            )
        except (TelegramBadRequest, KeyError) as _ex:
            await message.delete()
            msg = await message.answer(
                text=f'<b>К сожалению вы ввели некорректное значение языка</b>\n\n'
                     f'Введите ещё раз ❗️\n\n'
                     f'Верный формат <code>ru, en, uk</code>',
                reply_markup=await go_decode_settings_kb()
            )
    else:
        try:
            msg = await data['msg'].edit_text(
                text=f'<b>Запомнил язык:</b> <code>{message.text}</code>',
                reply_markup=await go_decode_settings_kb()
            )
        except (TelegramBadRequest, KeyError) as _ex:
            await message.delete()
            msg = await message.answer(
                text=f'<b>Запомнил язык:</b> <code>{message.text}</code>',
                reply_markup=await go_decode_settings_kb()
            )
        await state.update_data(lang=message.text)
    await state.update_data(msg=msg)


async def auto_lang(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_lang)
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Выбран вариант <code>·Автоопределение·</code></b>',
            reply_markup=await go_decode_settings_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Пожалуйста, укажите язык речи в формате "en", "ru" или нажмите "Автоопределение"</b>',
            reply_markup=await go_decode_settings_kb()
        )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_lang, F.data == 'choose_lang')
    dp.message.register(get_lang, FSMCreate.choose_lang, F.content_type == 'text')
    dp.callback_query.register(auto_lang, F.data == 'auto_lang')
