from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import go_decode_settings_kb, choose_speakers_kb
from utils.states.user import FSMCreate


async def choose_count_speakers(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_count_speakers)
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Пожалуйста, укажите количество спикеров или нажмите <code>·Автоопределение·</code></b>',
            reply_markup=await choose_speakers_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Пожалуйста, укажите количество спикеров или нажмите <code>·Автоопределение·</code></b>',
            reply_markup=await choose_speakers_kb()
        )
    await state.update_data(msg=msg)


async def get_count_speakers(message: types.Message, state: FSMContext):
    await state.set_state(FSMCreate.choose_count_speakers)
    data = await state.get_data()
    await message.delete()
    try:
        int(message.text)
        try:
            msg = await data['msg'].edit_text(
                text=f'<b>Запомнил количество спикеров:</b> <code>{message.text}</code>',
                reply_markup=await go_decode_settings_kb()
            )
        except (TelegramBadRequest, KeyError) as _ex:
            await message.delete()
            msg = await message.answer(
                text=f'<b>Запомнил количество спикеров:</b> <code>{message.text}</code>',
                reply_markup=await go_decode_settings_kb()
            )
        await state.update_data(count_speakers=message.text)
    except Exception as _ex:
        try:
            msg = await data['msg'].edit_text(
                text=f'<b>К сожалению вы ввели некорректное значение количества спикеров\n\n'
                     f'Введите ещё раз ❗️\n\n'
                     f'Верный формат: <code>1, 2, 3, 4, ...</code></b>',
                reply_markup=await go_decode_settings_kb()
            )
        except (TelegramBadRequest, KeyError) as _ex:
            await message.delete()
            msg = await message.answer(
                text=f'<b>К сожалению вы ввели некорректное значение количества спикеров\n\n'
                     f'Введите ещё раз ❗️\n\n'
                     f'Верный формат: <code>1, 2, 3, 4, ...</code></b>',
                reply_markup=await go_decode_settings_kb()
            )

    await state.update_data(msg=msg)


async def auto_speakers(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMCreate.choose_count_speakers)
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Выбран вариант <code>·Автоопределение·</code></b>',
            reply_markup=await go_decode_settings_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Выбран вариант <code>·Автоопределение·</code></b>',
            reply_markup=await go_decode_settings_kb()
        )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(choose_count_speakers, F.data == 'count_speakers')
    dp.message.register(get_count_speakers, FSMCreate.choose_count_speakers, F.content_type == 'text')
    dp.callback_query.register(auto_speakers, F.data == 'auto_speakers')
