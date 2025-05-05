from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot_start import logger
from integrations.database.models.minute import create_minute_db
from integrations.database.models.user import is_user_exists_db, create_user_db


class RegisterCheck(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        if data.get('session_maker'):
            session_maker = data['session_maker']

            if not await is_user_exists_db(user_id=event.from_user.id, session_maker=session_maker):
                if event.from_user.username is None:
                    username = 'None'
                else:
                    username = event.from_user.username
                if len(event.text.split(' ')) > 1:
                    try:
                        logger.info(f'Used UTM Mark --> {event.text.split(" ")[1]} --> {event.from_user.id}')
                    except Exception:
                        pass
                    try:
                        await create_user_db(user_id=event.from_user.id,
                                             username=username,
                                             session_maker=session_maker,
                                             utm=event.text.split(' ')[1])
                        await create_minute_db(telegram_id=event.from_user.id,
                                               session_maker=session_maker)
                    except Exception:
                        await create_user_db(user_id=event.from_user.id,
                                             username=username,
                                             session_maker=session_maker,
                                             utm='Error')
                        await create_minute_db(telegram_id=event.from_user.id,
                                               session_maker=session_maker)
                else:
                    await create_user_db(user_id=event.from_user.id,
                                         username=username,
                                         session_maker=session_maker,
                                         utm='None')
                    await create_minute_db(telegram_id=event.from_user.id,
                                           session_maker=session_maker)

                return await handler(event, data)
            else:
                return await handler(event, data)
