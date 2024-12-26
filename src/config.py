import logging
from dataclasses import dataclass
from os import getenv

from sqlalchemy.engine import URL

from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:

    name: str | None = getenv('PYMYSQL_DATABASE')
    user: str | None = getenv('PYMYSQL_USER')
    passwd: str | None = getenv('PYMYSQL_PASSWORD', None)
    port: int = int(getenv('PYMYSQL_PORT', 3306))
    host: str = getenv('PYMYSQL_HOST', 'test')
    driver: str = 'aiomysql'
    database_system: str = 'mysql'

    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)

@dataclass
class BotConfig:
    token: str = getenv('BOT_TOKEN')
    yookassa_token = getenv('YOOKASSA_TOKEN')
    yookassa_id = getenv('YOOKASSA_ID')
    gpt_token = getenv('GPT_API_KEY')

    yandex_access_key: str = getenv('YANDEX_ACCESS_KEY')
    yandex_secret_key: str = getenv('YANDEX_SECRET_KEY')
    yandex_region: str = getenv('YANDEX_REGION')
    yandex_bucket_name: str = getenv('YANDEX_BUCKET')


@dataclass
class Configuration:
    debug = bool(getenv('DEBUG'))
    logging_level = int(getenv('LOGGING_LEVEL', logging.INFO))
    yadisk_token = getenv('YADISK_TOKEN')
    replicate_token = getenv('REPLICATE_TOKEN')

    db = DatabaseConfig()
    bot = BotConfig()


@dataclass
class UserBotConfig:
    api_id = getenv('API_ID')
    api_hash = getenv('API_HASH')
    telegram_id = getenv('TELEGRAM_ID')
    bot_username = getenv('BOT_USERNAME')
conf = Configuration()
