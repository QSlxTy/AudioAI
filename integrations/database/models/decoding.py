from sqlalchemy import BigInteger, Text, update
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from datetime import datetime
from ..modeles import AbstractModel


class Decoding(AbstractModel):
    __tablename__ = 'decoding'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    status: Mapped[str] = mapped_column(Text(), default=None)
    date_create: Mapped[datetime] = mapped_column()
    replicate_id: Mapped[int] = mapped_column(BigInteger())


async def create_decoding_db(telegram_id: int, status: str, replicate_id: int, session_maker: sessionmaker) -> \
        [Decoding, Exception]:

    async with session_maker() as session:
        async with session.begin():
            decoding = Decoding(
                telegram_id=telegram_id,
                status=status,
                replicate_id=replicate_id,
                date_create=datetime.now()
            )
            try:
                session.add(decoding)
                return Decoding
            except ProgrammingError as _ex:
                return _ex


async def update_decoding_db(telegram_id: int, replicate_id: int, data: dict, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(Decoding).where(Decoding.telegram_id == telegram_id).where(
                Decoding.replicate_id == replicate_id).values(data))
            await session.commit()
