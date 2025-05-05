from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import choose_lang_kb, go_decode_settings_kb
from utils.aiogram_helper import languages
from utils.states.user import FSMCreate


async def choose_lang(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_lang)
    await call.message.answer(
        text='<b>🗣️ Пожалуйста, укажите язык речи в формате "en", "ru" или нажмите <code>·Автоопределение·</code>. Мы готовы подстроиться под ваши нужды! 😊</b>',
        reply_markup=await choose_lang_kb()
    )


async def get_lang(message: types.Message, state: FSMContext):
    if message.text not in languages:
        await message.answer(
            text=f'😅 <b>К сожалению, вы ввели некорректное значение языка.</b>\n\n'
                 f'Попробуйте еще раз, пожалуйста ❗️\n\n'
                 f'Пример верного формата: <code>ru, en, uk</code>',
            reply_markup=await go_decode_settings_kb()
        )
    else:
        await message.answer(
            text=f'👍 <b>Отлично! Я запомнил ваш язык:</b> <code>{message.text}</code>',
            reply_markup=await go_decode_settings_kb()
        )
        await state.update_data(lang=message.text)


async def auto_lang(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_lang)
    await call.message.answer(
        text='✅ Вы выбрали вариант <code>·Автоопределение·</code>. Мы все настроим сами!',
        reply_markup=await go_decode_settings_kb()
    )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_lang, F.data == 'choose_lang')
    dp.message.register(get_lang, FSMCreate.choose_lang, F.content_type == 'text',~F.text.startswith('/'))
    dp.callback_query.register(auto_lang, F.data == 'auto_lang')
