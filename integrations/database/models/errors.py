from datetime import datetime

from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class Errors(AbstractModel):
    __tablename__ = 'errors'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    other: Mapped[str] = mapped_column(Text())
    handler_error: Mapped[str] = mapped_column(Text())
    text_error: Mapped[str] = mapped_column(Text())
    date_create: Mapped[datetime] = mapped_column()


async def create_error_db(telegram_id: int, other: str, handler_error: str, text_error: str,
                          session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            error = Errors(
                telegram_id=telegram_id,
                other=other,
                handler_error=handler_error,
                text_error=text_error,
                date_create=datetime.now()
            )
            session.add(error)
