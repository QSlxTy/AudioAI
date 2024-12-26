from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.tariff import get_tariff_db
from keyboards.user.user_keyboard import accept_rules_kb, get_email_kb, payment_link_kb, back_menu_kb
from utils.states.user import FSMTariff
from utils.yookassa_api import create_yookassa_link, check_payment_yookassa


async def get_email(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    await state.set_state(FSMTariff.get_email)
    tariff_info = await get_tariff_db(call.data.split(":")[1], session_maker)
    await call.message.answer(
        text=f'<b>Выбран тариф - <code>{tariff_info.tariff_name}</code> минут\n'
             f'Стоимость - <code>{tariff_info.price}</code> RUB\n\n'
             f'Укажите ваш Email для получения чека</b>',
        reply_markup=await get_email_kb()
    )
    await state.update_data(tariff=call.data.split(":")[1])


async def accept_create_call(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text=f'<b>Нажмия кнопку <code>·Подтвердить·</code> - вы соглашаетесь с правилами нашего сообщества\n\n'
             f'·Оферта: <a href= "https://docs.google.com/document/'
             f'd/1G8AKLJWVZSRdO1Wp_enzu5bHpI_roaSqcgcSBq3h2n0/edit"> Ссылка </a>\n'
             f'·Политика обработки данных: <a href= "https://docs.google.com/'
             f'document/d/1MhSU_GgHO5nHynFXEPZm0GX8JYLonTRRaUmbyMlzA-4/edit?usp=sharing"> Ссылка </a></b>',
        disable_web_page_preview=True,
        reply_markup=await accept_rules_kb()
    )
    await state.update_data(email='kirya_kirya_228tk@mail.ru')


async def accept_create_message(message: types.Message, state: FSMContext):
    await state.set_state(FSMTariff.get_email)
    if '@' not in message.text:
        await message.answer(
            text=f'<b>Неверный формат Email ❗️\n\n'
                 f'Попробуйте ещё раз</b>',
            reply_markup=await back_menu_kb()
        )
    else:
        await message.answer(
            text=f'<b>Нажмия кнопку <code>·Подтвердить·</code> - вы соглашаетесь с правилами нашего сообщества\n\n'
                 f'·Оферта: <a href= "https://docs.google.com/document/'
                 f'd/1G8AKLJWVZSRdO1Wp_enzu5bHpI_roaSqcgcSBq3h2n0/edit"> Ссылка </a>\n'
                 f'·Политика обработки данных: <a href= "https://docs.google.com/'
                 f'document/d/1MhSU_GgHO5nHynFXEPZm0GX8JYLonTRRaUmbyMlzA-4/edit?usp=sharing"> Ссылка </a></b>',
            disable_web_page_preview=True,
            reply_markup=await accept_rules_kb()
        )
        await message.delete()
    await state.update_data(email=message.text)


async def create_payment_link(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    tariff_info = await get_tariff_db(data['tariff'], session_maker)
    result = await create_yookassa_link(tariff_info.price, data['email'], call.from_user.id, data['tariff'],
                                        session_maker)
    if result is not None:
        await call.message.answer(
            text=f'<b>Ваша ссылка для оплаты.\n'
                 f'После совершения оплаты, нажмите кнопку <code>·Проверить оплату·</code>\n\n'
                 f'Также обязательно сохраните скриншот оплаты ❗️</b>',
            reply_markup=await payment_link_kb(result[0], 0)
        )
        await state.update_data(payment_id=result[1], url=result[0], seconds=tariff_info.seconds)
    else:
        await call.message.answer(
            text=f'<b>Ошибка создания ссылки платежа, обратитесь в поддержку ❗️</b>',
            reply_markup=await back_menu_kb()
        )


async def check_payment(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    result = await check_payment_yookassa(data['payment_id'], call.from_user.id, data['seconds'], session_maker)
    if result is True:
        await call.message.answer(
            text=f'<b>Оплата прошла. Минуты зачислены вам на баланс\n\n'
                 f'Чек\n'
                 f'Пользователь - <code>{call.from_user.username}</code>\n'
                 f'ID операции - <code>{data["payment_id"]}</code>\n'
                 f'Тариф - <code>{data["tariff"]} минут</code>\n'
                 f'Статус - <code>Оплачено</code></b>',
            reply_markup=await back_menu_kb()
        )
    else:
        await call.message.answer(
            text=f'<b>Оплата ещё не прошла, провертье оплату позже</b>',
            reply_markup=await payment_link_kb(data['url'], data['payment_id'])
        )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(get_email, F.data.startswith('choose_tariff'))
    dp.callback_query.register(accept_create_call, F.data == 'no_check')
    dp.message.register(accept_create_message, FSMTariff.get_email, F.content_type == 'text')
    dp.callback_query.register(create_payment_link, F.data == 'accept_create')
    dp.callback_query.register(check_payment, F.data == 'check_payment')
