import asyncio
import logging
from datetime import datetime
from src.config import UserBotConfig

from bot_start import dp, bot, client
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
    '''INITIALIZE USER BOT'''
    await client.start(password=UserBotConfig.bot_password)
    await client.connect()
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
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        client.disconnect()
        logging.info('Bot stopped')
