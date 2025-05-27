import json
from logging import getLogger

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from dateutil.relativedelta import relativedelta

from bot.config import Settings
from bot.controllers.user import reset_user_image_counter, update_user_expiration
from bot.internal.callbacks import PaidEntityCallbackFactory
from bot.internal.enums import PaidEntity, AIState
from bot.internal.lexicon import payment_text, replies
from database.models import User

router = Router()
logger = getLogger(__name__)


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.callback_query(PaidEntityCallbackFactory.filter())
async def payment_handler(
    callback: CallbackQuery,
    callback_data: PaidEntityCallbackFactory,
    settings: Settings,
):
    await callback.answer()
    match callback_data.entity:
        case PaidEntity.ONE_MONTH_SUBSCRIPTION:
            description = "Длительность: 1 месяц"
            value = 390
            prices = [
                LabeledPrice(label="Подписка на 1 месяц", amount=value * 100),
            ]
        case PaidEntity.ONE_YEAR_SUBSCRIPTION:
            description = "Длительность: 1 год"
            value = 3900
            prices = [
                LabeledPrice(label="Подписка на 1 год", amount=value * 100),
            ]
        case PaidEntity.PICTURES_COUNTER_REFRESH:
            description = "Сброс лимита картинок"
            value = 150
            prices = [
                LabeledPrice(label="Дополнительные 50 картинок", amount=value * 100),
            ]
        case _:
            assert False, "Unexpected paid entity"
    provider_data = {
        "receipt": {
            "items": [
                {
                    "description": description,
                    "quantity": 1,
                    "amount": {
                        "value": value,
                        "currency": "RUB",
                    },
                    "vat_code": 1,
                    "payment_mode": "full_payment",
                    "payment_subject": "service"
                }
            ],
            "capture": True,
            "save_payment_method": True,
            "tax_system_code": 1
        }
    }
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Оплата",
        description=description,
        payload=callback_data.entity,
        provider_token=settings.bot.PROVIDER_TOKEN.get_secret_value(),
        currency="RUB",
        prices=prices,
        need_email=True,
        send_email_to_provider=True,
        provider_data=json.dumps(provider_data),
    )


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message,
    user: User,
    state: FSMContext,
    settings: Settings,
    db_session: AsyncSession,
):
    payment = message.successful_payment
    response = "💳 Данные платежа:\n\n"

    # Выводим все атрибуты основного объекта платежа
    for attr_name in dir(payment):
        if not attr_name.startswith('_'):  # Исключаем служебные поля
            attr_value = getattr(payment, attr_name)
            if not callable(attr_value):  # Исключаем методы
                response += f"🔹 {attr_name}: {attr_value}\n"

    # Обработка order_info (если есть)
    if hasattr(payment, 'order_info') and payment.order_info:
        response += "\n📦 Информация о заказе:\n"
        for attr_name in dir(payment.order_info):
            if not attr_name.startswith('_'):
                attr_value = getattr(payment.order_info, attr_name)
                if not callable(attr_value) and attr_value is not None:
                    response += f"  • {attr_name}: {attr_value}\n"

    await message.answer(response)

    # payment = message.successful_payment
    # response = "💳 Все данные платежа:\n\n"
    #
    # # Пытаемся получить словарь атрибутов
    # payment_vars = vars(payment) if hasattr(payment, '__dict__') else {}
    #
    # for attr_name, attr_value in payment_vars.items():
    #     response += f"🔹 {attr_name}: {attr_value}\n"
    #
    # await message.answer(response if payment_vars else "Не удалось получить данные платежа")
    #
    #



    # payload = message.successful_payment.invoice_payload
    # if payload in (PaidEntity.ONE_MONTH_SUBSCRIPTION, PaidEntity.ONE_YEAR_SUBSCRIPTION):
    #     text = (
    #         payment_text["1 month success"]
    #         if payload == PaidEntity.ONE_MONTH_SUBSCRIPTION
    #         else payment_text["1 year success"]
    #     )
    #     dutation = relativedelta(months=1) if payload == PaidEntity.ONE_MONTH_SUBSCRIPTION else relativedelta(years=1)
    #     await update_user_expiration(user, dutation, db_session)
    #     await message.answer_photo(FSInputFile(path='src/bot/data/gardener1.png'), text)
    #     await state.set_state(AIState.IN_AI_DIALOG)
    #     logger.info(f"Successful payment for user {user.username}: {message.successful_payment.invoice_payload}")
    # else:
    #     await reset_user_image_counter(user.tg_id, db_session)
    #     await message.answer_photo(
    #         FSInputFile(path='src/bot/data/taking_photo.png'), payment_text["refresh_pictures_limit_success"]
    #     )
    #     logger.info(f"Successful payment for user {user.username}: {message.successful_payment.invoice_payload}")
    # await message.bot.send_message(
    #     settings.bot.CHAT_LOG_ID,
    #     replies["user_payment_log"].format(
    #         username=user.username,
    #         payload=message.successful_payment.invoice_payload,
    #     ),
    # )
    # await state.set_state(AIState.IN_AI_DIALOG)
    #
