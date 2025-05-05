import json

from yookassa import Configuration, Payment

from bot_start import logger
from integrations.database.models.minute import update_minute_db, get_minute_db
from integrations.database.models.payment import create_payment_db, update_payment_db
from integrations.database.models.user import update_user_db
from src.config import BotConfig

Configuration.account_id = BotConfig.yookassa_id
Configuration.secret_key = BotConfig.yookassa_token


async def create_yookassa_link(amount, email, user_id, tariff_name, session_maker, return_url='https://your.return.url'):
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "receipt": {
            "customer": {
                "email": email,
            },
            "items": [
                {

                    "description": "Покупка минут",
                    "quantity": "1",
                    "amount": {
                        "value": amount,
                        "currency": "RUB",
                    },
                    "vat_code": "1",
                },
            ]

        },
        "capture": True,
        "description": "Покупка минут"
    })

    try:
        payment_data = json.loads(payment.json())
        await create_payment_db(user_id, email, payment_data['id'], amount, tariff_name, session_maker)
        logger.info(f'Payment link created --> {payment_data["confirmation"]["confirmation_url"]}')
        return [payment_data['confirmation']['confirmation_url'], payment_data['id']]
    except Exception as _ex:
        logger.error(f'Create link ERROR --> {_ex}')
        return None


async def check_payment_yookassa(payment_id, user_id, seconds, session_maker):
    output = Payment.find_one(payment_id)
    payment_data = json.loads(output.json())
    try:
        if payment_data['status'] == "succeeded":
            await update_payment_db(payment_id, {'status': 'success'}, session_maker)
            user_info = await get_minute_db({'telegram_id': user_id}, session_maker)
            await update_minute_db(user_id, {'remaining_seconds': user_info.remaining_seconds + seconds}, session_maker)
            logger.error(f'Payment SUCCESS user_id --> {user_id}')
            return True
        else:
            return False
    except Exception as _ex:
        logger.error(f'Payment check ERROR --> {_ex}')
        await update_payment_db(payment_id, {'status': 'success'}, session_maker)
        return False
