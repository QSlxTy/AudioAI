from datetime import datetime

from sqlalchemy import BigInteger, Text, SmallInteger
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from ..modeles import AbstractModel


class Action(AbstractModel):
    __tablename__ = 'action'

    telegram_id: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[datetime] = mapped_column()
    duration: Mapped[int] = mapped_column(BigInteger())
    language: Mapped[str] = mapped_column(Text())
    num_speakers: Mapped[str] = mapped_column(Text())
    special_words: Mapped[str] = mapped_column(Text())
    decoding_format: Mapped[str] = mapped_column(Text())
    summary_format: Mapped[str] = mapped_column(Text())
    count_files: Mapped[int] = mapped_column(SmallInteger())


async def create_action_db(telegram_id: int, count_files: int, duration: int, language: str,
                           num_speakers: int, special_words: str, decoding_format: str, summary_format: str,
                           session_maker: sessionmaker) -> [Action, Exception]:
    if num_speakers == '':
        num_speakers = 'auto'
    if language == '':
        language = 'auto'
    if special_words == '':
        special_words = '-'
    async with session_maker() as session:
        async with session.begin():
            action = Action(
                created_at=datetime.now(),
                telegram_id=telegram_id,
                duration=duration,
                language=language,
                num_speakers=num_speakers,
                special_words=special_words,
                decoding_format=decoding_format,
                summary_format=summary_format,
                count_files=count_files

            )
            try:
                session.add(action)
                return Action
            except ProgrammingError as _ex:
                return _ex
