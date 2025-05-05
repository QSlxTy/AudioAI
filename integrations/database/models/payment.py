from datetime import datetime

from sqlalchemy import BigInteger, Float, Text, update, String
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column

from ..modeles import AbstractModel


class Payment(AbstractModel):
    __tablename__ = 'payment'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    payment_id: Mapped[str] = mapped_column(String(39), unique=True)
    amount: Mapped[float] = mapped_column(Float())
    created_at: Mapped[datetime] = mapped_column()
    tariff_name: Mapped[str] = mapped_column(Text())
    email: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Text())


async def create_payment_db(telegram_id: str, email: str, payment_id: str, amount: float, tariff_name, session_maker) -> \
        [Payment, Exception]:
    async with session_maker() as session:
        async with session.begin():
            payment = Payment(
                created_at=datetime.now(),
                telegram_id=telegram_id,
                payment_id=payment_id,
                amount=amount,
                tariff_name=tariff_name,
                email=email,
                status='in proccess'
            )
            try:
                session.add(payment)
                return Payment
            except ProgrammingError as _ex:
                return _ex


async def update_payment_db(payment_id: int, data: dict, session_maker) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(Payment).where(Payment.payment_id == payment_id).values(data))
            await session.commit()
