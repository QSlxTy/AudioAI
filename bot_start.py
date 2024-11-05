import logging


from telethon import TelegramClient

from src.bot.dispatcher import get_dispatcher

from src.config import conf, UserBotConfig
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot
client = TelegramClient('AudioSession', UserBotConfig.api_id, UserBotConfig.api_hash, system_version="4.16.30-vxCUSTOM")
bot = Bot(token=conf.bot.token, parse_mode='HTML')
storage = MemoryStorage()
logger = logging.getLogger(__name__)
dp = get_dispatcher(storage=storage)
