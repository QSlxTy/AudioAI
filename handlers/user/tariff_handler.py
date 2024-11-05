from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import tariff_list_kb


async def tariff_info(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text='<b>Вы можете приобрести дополнительные минуты здесь. \n'
                 'Все купленные минуты будут суммированы с уже имеющимися у вас минутами.\n\n'
                 '·Пакет 30 минут: 247.17 рублей\n'
                 '·Пакет 120 минут: 988.68 рублей\n'
                 '·Пакет 480 минут: 3954.72 рублей\n'
                 '·Пакет 3000 минут: 24717 рублей\n</b>',
            reply_markup=await tariff_list_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Вы можете приобрести дополнительные минуты здесь. \n'
                 'Все купленные минуты будут суммированы с уже имеющимися у вас минутами.\n\n'
                 '·Пакет 30 минут: 247.17 рублей\n'
                 '·Пакет 120 минут: 988.68 рублей\n'
                 '·Пакет 480 минут: 3954.72 рублей\n'
                 '·Пакет 3000 минут: 24717 рублей\n</b>',
            reply_markup=await tariff_list_kb()
        )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(tariff_info, F.data == 'check_tariff')