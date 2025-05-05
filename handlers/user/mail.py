import os
from asyncio import sleep

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from sqlalchemy.orm import sessionmaker

from bot_start import bot, logger
from integrations.database.models.user import get_all_users_db, update_user_db
from keyboards.user.user_keyboard import back_menu_kb, choose_mail_kb
from utils.states.admin import FSMMail


async def start_mail(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMMail.get_email)
    await call.message.answer(
        text=f'<b>Отправьте медиафайл 📷\n'
             f'Если с медиафайлом, то прикрепите текст к медиафайлу\n'
             f'Если медиафайл не требуется, то просто отправьте текст рассылки</b>',
        reply_markup=await back_menu_kb()
    )


async def main_mail_media(message: types.Message, state: FSMContext):
    if message.photo:
        file = await bot.get_file(
            file_id=message.photo[-1].file_id,
            request_timeout=300
        )
        await message.answer_photo(
            photo=FSInputFile(file.file_path.replace('\\', '/')),
            caption=f'<b>Проверим рассылку</b>\n'
                    f'{message.caption}',
            reply_markup=await choose_mail_kb()
        )
        await state.update_data(file_path=file.file_path.replace('\\', '/'), text_mail=message.caption)

    elif message.video:
        file = await bot.get_file(
            file_id=message.video.file_id,
            request_timeout=300
        )
        await message.answer_video(
            video=FSInputFile(file.file_path.replace('\\', '/')),
            caption=f'<b>Проверим рассылку</b>\n'
                    f'{message.caption}',
            reply_markup=await choose_mail_kb()
        )
        await state.update_data(file_path=file.file_path.replace('\\', '/'), text_mail=message.caption)
    else:
        await message.answer(
            text=f'<b>Проверим рассылку</b>\n'
                 f'{message.text}',
            reply_markup=await choose_mail_kb()
        )
        await state.update_data(file_path=False, text_mail=message.text)


async def go_mail(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    data = await state.get_data()
    if call.data.split(':')[1] == 'True':
        await call.message.answer(
            text=f'<b>Рассылка запущена ⚙️'
                 f'После завершения рассылки вы получите уведомление</b>\n',
            reply_markup=await back_menu_kb()
        )
        count_true_users, count_all_users = await mail_func(data['file_path'], data['text_mail'], session_maker)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'<b>Рассылка завершена ✔️</b>\n\n'
                 f'✉️ Отправлено сообщений: <code>{count_all_users}</code>\n'
                 f'📩 Получено сообщений: <code>{count_true_users}</code>',
            reply_markup=await back_menu_kb()
        )
        return
    await call.message.answer(
        text=f'<b>Рассылка отменена! </b>',
        reply_markup=await back_menu_kb()
    )


def register_handler(dp: Dispatcher):
    dp.callback_query.register(start_mail, F.data == 'mail')
    dp.message.register(main_mail_media, F.content_type.in_({'photo', 'video', 'text'}), ~F.text.startswith('/'),
                        FSMMail.get_email)
    dp.callback_query.register(go_mail, F.data.startswith('go_mail'))


async def mail_func(file_path, text_mail, session_maker):
    users_list = await get_all_users_db(session_maker)
    count_true_users = 0
    count_all_users = 0
    for user in users_list:
        if user.is_admin is False and user.is_block is False:
            count_all_users += 1
            if file_path is False:
                try:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f'{text_mail}'
                    )
                    count_true_users += 1
                    await sleep(2)
                except Exception as _ex:
                    await update_user_db(user.telegram_id, {'is_block': True}, session_maker)
                    logger.error(f"Error send mail --> {_ex}")

            else:
                if file_path.split('.')[-1] == 'jpg' or file_path.split('.')[-1] == 'png':
                    try:
                        await bot.send_photo(
                            chat_id=user.telegram_id,
                            photo=FSInputFile(file_path),
                            caption=f'{text_mail}'
                        )
                        count_true_users += 1
                        await sleep(2)
                    except Exception as _ex:
                        await update_user_db(user.telegram_id, {'is_block': True}, session_maker)
                        logger.error(f"Error send mail --> {_ex}")
                else:
                    try:
                        await bot.send_video(
                            chat_id=user.telegram_id,
                            video=FSInputFile(file_path),
                            caption=f'{text_mail}'
                        )
                        count_true_users += 1
                        await sleep(2)
                    except Exception as _ex:
                        await update_user_db(user.telegram_id, {'is_block': True}, session_maker)
                        logger.error(f"Error send mail --> {_ex}")

    try:
        os.remove(file_path)
    except Exception:
        logger.error('Delete mail file error')
    return count_true_users, count_all_users
