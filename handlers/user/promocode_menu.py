from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.minute import get_minute_db, update_minute_db
from integrations.database.models.promo import get_promo_db, update_promo_db, is_promo_exists_db
from integrations.database.models.used_promo import is_used_promo_exists_db, create_used_promo_db
from keyboards.user.user_keyboard import back_menu_kb, back_tariff_menu_kb
from utils.states.user import FSMPromo


async def menu_promo(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FSMPromo.menu_promo)
    try:
        msg = await data['msg'].edit_text(
            text='<b>Пожалуйста, введите промокод для получения дополнительных минут</b>',
            reply_markup=await back_tariff_menu_kb()
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text='<b>Пожалуйста, введите промокод для получения дополнительных минут</b>',
            reply_markup=await back_tariff_menu_kb()
        )

    await state.update_data(msg=msg)


async def get_promo(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    if await is_used_promo_exists_db(message.text, message.from_user.id, session_maker):
        await message.delete()
        try:
            msg = await data['msg'].edit_text(
                text='<b>Вы уже использовали этот промокод</b>',
                reply_markup=await back_menu_kb()
            )
        except (TelegramBadRequest, KeyError) as _ex:
            await message.delete()
            msg = await message.answer(
                text='<b>Вы уже использовали этот промокод</b>',
                reply_markup=await back_menu_kb()
            )
    else:
        if await is_promo_exists_db(message.text, session_maker):
            promo_info = await get_promo_db({'promo': message.text}, session_maker)
            user_info = await get_minute_db({'telegram_id': message.from_user.id}, session_maker)
            await create_used_promo_db(message.from_user.id, message.text, session_maker)
            await update_minute_db(message.from_user.id,
                                   {'remaining_seconds': user_info.remaining_seconds + promo_info.seconds},
                                   session_maker)
            await update_promo_db(message.text, {'count': promo_info.count - 1}, session_maker)
            await message.delete()
            try:
                msg = await data['msg'].edit_text(
                    text=f'<b>Промокод успешно активирован, вы получили '
                         f'<code>{round(promo_info.seconds / 60, 2)} минут</code></b>',
                    reply_markup=await back_menu_kb()
                )
            except (TelegramBadRequest, KeyError) as _ex:
                await message.delete()
                msg = await message.answer(
                    text=f'<b>Промокод успешно активирован, вы получили '
                         f'<code>{round(promo_info.seconds / 60, 2)} минут</code></b>',
                    reply_markup=await back_menu_kb()
                )
        else:
            await message.delete()
            try:
                msg = await data['msg'].edit_text(
                    text='<b>К сожалению такого промокода несуществует</b>',
                    reply_markup=await back_menu_kb()
                )
            except (TelegramBadRequest, KeyError) as _ex:
                await message.delete()
                msg = await message.answer(
                    text='<b>К сожалению такого промокода несуществует</b>',
                    reply_markup=await back_menu_kb()
                )
    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(menu_promo, F.data == 'go_promo')
    dp.message.register(get_promo, FSMPromo.menu_promo, F.content_type == 'text')
