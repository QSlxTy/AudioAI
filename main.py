import asyncio
import logging
import os
import shutil

from bot_start import dp, bot
from handlers.register_handlers import register_handlers
from integrations.database.sql_alch import create_connection, init_models, get_session_maker
from src.bot.structures.data_structure import TransferData
from src.config import conf
from utils.middlewares.database_md import DatabaseMiddleware
from utils.middlewares.register_check_md import RegisterCheck


async def start_bot():
    connection = await create_connection()
    ''' REGISTER MIDDLEWARES and HANDLERS'''
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())
    await register_handlers(dp)
    ''' INITIALIZE DATABASE MODELS and CREATE SESSION '''
    await init_models(connection)
    session_maker = get_session_maker(connection)
    ''' START BOT PENDING and DROP PENDING UPDATES BY DELETING WEBHOOK'''
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True,
                           **TransferData(engine=connection), session_maker=session_maker
                           )

if __name__ == '__main__':
    try:
        logging.basicConfig(level=conf.logging_level)
        logging.getLogger('httpcore.http11').disabled = True
        logging.getLogger('telethon.network.mtprotosender').disabled = True
        logging.getLogger('telethon.extensions.messagepacker').disabled = True
        logging.getLogger('telethon.messagebox').disabled = True
        logging.getLogger('charset_normalizer').disabled = True
        logging.getLogger('pydub.converter').disabled = True
        logging.getLogger('telethon.client.updates').disabled = True
        logging.getLogger('botocore').setLevel(logging.WARNING)
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('aioboto3').setLevel(logging.WARNING)
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        for folder in os.listdir('root/bot_audio_v2/local'):
            folder_path = os.path.join('root/bot_audio_v2/local', folder)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
                os.makedirs(folder_path)

        logging.info('Bot stopped')
