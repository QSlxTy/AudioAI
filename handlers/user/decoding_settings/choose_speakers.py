from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from bot_start import logger
from keyboards.user.user_keyboard import go_decode_settings_kb, choose_speakers_kb
from utils.states.user import FSMCreate


async def choose_count_speakers(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSMCreate.choose_count_speakers)
    logger.info(f'Speakers settings --> {call.from_user.id}')

    msg = await data['msg'].edit_text(
        text='<b>👥 Введите количество спикеров текстом или выберите <code>автоопределение</code>. Это поможет нам правильно обработать файл. 😊</b>',
        reply_markup=await choose_speakers_kb()
    )
    await state.update_data(msg=msg)


async def get_count_speakers(message: types.Message, state: FSMContext):
    data = await state.get_data()

    try:
        int(message.text)
        msg = await data['msg'].edit_text(
            text=f'👍 <b>Я запомнил количество спикеров:</b> <code>{message.text}</code>',
            reply_markup=await go_decode_settings_kb()
        )
        await state.update_data(count_speakers=message.text)
    except Exception as _ex:
        msg = await data['msg'].edit_text(
            text=f'😔 <b>К сожалению, вы ввели некорректное значение количества спикеров.</b>\n\n'
                 f'Попробуйте еще раз ❗️\n\n'
                 f'Пример верного формата: <code>1, 2, 3, 4...</code>',
            reply_markup=await go_decode_settings_kb()
        )
        await state.set_state(FSMCreate.choose_count_speakers)
    await state.update_data(msg=msg)


async def auto_speakers(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await state.set_state(FSMCreate.choose_count_speakers)
    msg = await data['msg'].edit_text(
        text='<b>✅ Вы выбрали вариант <code>·Автоопределение·</code>. Мы все настроим сами!</b>',
        reply_markup=await go_decode_settings_kb()
    )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_count_speakers, F.data == 'count_speakers')
    dp.message.register(get_count_speakers, FSMCreate.choose_count_speakers, F.content_type == 'text',~F.text.startswith('/'))
    dp.callback_query.register(auto_speakers, F.data == 'auto_speakers')
