from sqlalchemy import BigInteger, update, select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class Minute(AbstractModel):
    __tablename__ = 'minute'

    telegram_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    remaining_seconds: Mapped[int] = mapped_column(BigInteger())


async def get_minute_db(select_by: dict, session_maker: sessionmaker) -> Minute:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Minute).filter_by(**select_by)
            )
            return result.scalars().one()


async def create_minute_db(telegram_id: int, session_maker: sessionmaker) -> [Minute, Exception]:
    async with session_maker() as session:
        async with session.begin():
            minute = Minute(
                telegram_id=telegram_id,
                remaining_seconds=60000,
            )
            try:
                session.add(minute)
                return Minute
            except ProgrammingError as _e:
                return _e


async def update_minute_db(telegram_id: int, data: dict, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(Minute).where(Minute.telegram_id == telegram_id).values(data))
            await session.commit()
