from datetime import datetime

from sqlalchemy import BigInteger, Text
from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class UsedPromo(AbstractModel):
    __tablename__ = 'used_promos'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    date_use: Mapped[datetime] = mapped_column()
    promo: Mapped[str] = mapped_column(Text)


async def get_used_promo_db(select_by: dict, session_maker: sessionmaker) -> UsedPromo:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(UsedPromo).filter_by(**select_by)
            )
            return result.scalars().all()


async def create_used_promo_db(user_id: int, promo: str, session_maker: sessionmaker) -> [UsedPromo, Exception]:
    async with session_maker() as session:
        async with session.begin():
            promo = UsedPromo(
                telegram_id=user_id,
                promo=promo,
                date_use=datetime.now(),
            )
            try:
                session.add(promo)
                return UsedPromo
            except ProgrammingError as _e:
                return _e


async def is_used_promo_exists_db(promo: str, telegram_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(
                select(UsedPromo).where(UsedPromo.promo == promo).where(UsedPromo.telegram_id == telegram_id))
            return bool(sql_res.first())
