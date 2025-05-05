import sqlalchemy.ext.asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from integrations.database.models.action import Action
from integrations.database.models.decoding import Decoding
from integrations.database.models.errors import Errors
from integrations.database.models.minute import Minute
from integrations.database.models.payment import Payment
from integrations.database.models.promo import Promo
from integrations.database.models.tariff import Tariff
from integrations.database.models.used_promo import UsedPromo
from integrations.database.models.user import User
from src.config import conf


def get_session_maker(engine: sqlalchemy.ext.asyncio.AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=sqlalchemy.ext.asyncio.AsyncSession, expire_on_commit=False)


async def create_connection() -> sqlalchemy.ext.asyncio.AsyncEngine:
    url = conf.db.build_connection_str()

    engine = _create_async_engine(
        url=url, pool_pre_ping=True)
    return engine


class Database:
    def __init__(
            self,
            session: AsyncSession,
            user: User = None,
            action: Action = None,
            decoding: Decoding = None,
            minute: Minute = None,
            payment: Payment = None,
            promo: Promo = None,
            tariff: Tariff = None,
            used_promo: UsedPromo = None,
            errors: Errors = None

    ):
        self.session = session
        self.user = user or User()
        self.action = action or Action()
        self.decoding = decoding or Decoding()
        self.minute = minute or Minute()
        self.payment = payment or Payment()
        self.promo = promo or Promo()
        self.tariff = tariff or Tariff()
        self.used_promo = used_promo or UsedPromo()
        self.errors = errors or Errors()


async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Action.metadata.create_all)
        await conn.run_sync(Decoding.metadata.create_all)
        await conn.run_sync(Minute.metadata.create_all)
        await conn.run_sync(Payment.metadata.create_all)
        await conn.run_sync(Promo.metadata.create_all)
        await conn.run_sync(Tariff.metadata.create_all)
        await conn.run_sync(UsedPromo.metadata.create_all)
        await conn.run_sync(Errors.metadata.create_all)