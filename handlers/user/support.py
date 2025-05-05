from aiogram import types, Dispatcher, F
from aiogram.filters import Command

from keyboards.user.user_keyboard import back_menu_kb


async def support_info_call(call: types.CallbackQuery):
    await call.message.answer(
        text="🤝 Если у вас возникли вопросы, загляните в <a href='https://teletype.in/@slush_ai_bot/faq'>[FAQ]</a>.\n\n"
             "Или просто напишите нам: @georgeraz. Мы всегда рядом и готовы помочь! 💌",
        reply_markup=await back_menu_kb(),
        disable_web_page_preview=True
    )


async def support_info_command(message: types.Message):
    await message.answer(
        text="🤝 Если у вас возникли вопросы, загляните в <a href='https://teletype.in/@slush_ai_bot/faq'>[FAQ]</a>.\n\n"
             "Или просто напишите нам: @georgeraz. Мы всегда рядом и готовы помочь! 💌",
        reply_markup=await back_menu_kb(),
        disable_web_page_preview=True
    )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(support_info_call, F.data == 'support')
    dp.message.register(support_info_command, Command('support'))
