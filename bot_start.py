import logging
import os
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from telethon import TelegramClient
from telethon.sessions import StringSession
from src.bot.dispatcher import get_dispatcher

from src.config import conf, UserBotConfig
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot
# client = TelegramClient('/root/bot_audio/AudioSession.session', UserBotConfig.api_id, UserBotConfig.api_hash,
#                         system_version="4.16.30-vxCUSTOM")
session = AiohttpSession(
    api=TelegramAPIServer.from_base('http://localhost:8081'))
bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode='HTML'), session=session)
storage = MemoryStorage()
logger = logging.getLogger(__name__)
dp = get_dispatcher(storage=storage)
