from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from keyboards.user.user_keyboard import back_menu_kb


async def support_info(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        msg = await data['msg'].edit_text(
            text=
            '<b>Перед тем как обратиться в нашу техподдержку, '
            'пожалуйста, ознакомьтесь с FAQ: https://teletype.in/@slush_ai_bot/faq '
            'Если у вас возникли трудности или вопросы, мы всегда готовы помочь! Просто напишите нам в поддержку: 👇'
            '@добавлю позже </b>',
            reply_markup=await back_menu_kb(),
            disable_web_page_preview=True
        )
    except (TelegramBadRequest, KeyError) as _ex:
        await call.message.delete()
        msg = await call.message.answer(
            text=
            '<b>Перед тем как обратиться в нашу техподдержку, '
            'пожалуйста, ознакомьтесь с FAQ: https://teletype.in/@slush_ai_bot/faq '
            'Если у вас возникли трудности или вопросы, мы всегда готовы помочь! Просто напишите нам в поддержку: 👇'
            '@добавлю позже </b>',
            reply_markup=await back_menu_kb(),
            disable_web_page_preview=True
        )

    await state.update_data(msg=msg)


def register_handler(dp: Dispatcher):
    dp.callback_query.register(support_info, F.data == 'support')
