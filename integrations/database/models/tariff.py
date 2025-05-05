from sqlalchemy import Float, Text, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class Tariff(AbstractModel):
    __tablename__ = 'tariff'

    tariff_name: Mapped[str] = mapped_column(Text(), default=None)
    price: Mapped[float] = mapped_column(Float(), default=None)


async def get_tariff_db(tariff_name: str, session_maker: sessionmaker) -> Tariff:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Tariff).where(Tariff.tariff_name == tariff_name)
            )
            return result.scalars().one()


async def get_all_tariff_db(session_maker: sessionmaker) -> [Tariff]:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Tariff)
            )
            return result.scalars().all()
