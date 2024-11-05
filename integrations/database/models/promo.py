from sqlalchemy import BigInteger, Text, Float, select, update
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class Promo(AbstractModel):
    __tablename__ = 'promo'

    promo: Mapped[str] = mapped_column(Text(), default=None)
    seconds: Mapped[float] = mapped_column(Float(), default=None)
    count: Mapped[int] = mapped_column(BigInteger())


async def get_promo_db(select_by: dict, session_maker: sessionmaker) -> Promo:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Promo).filter_by(**select_by)
            )
            return result.scalars().one()


async def update_promo_db(promo: str, data: dict, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(Promo).where(Promo.promo == promo).values(data))
            await session.commit()


async def is_promo_exists_db(promo: str, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(
                select(Promo).where(Promo.promo == promo))
            return bool(sql_res.first())
