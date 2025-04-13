from logging import getLogger

from aiogram import F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings
from bot.internal.callbacks import SubscriptionCallbackFactory
from bot.internal.enums import SubscriptionPlan
from database.models import User

router = Router()
logger = getLogger(__name__)


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.callback_query(SubscriptionCallbackFactory.filter())
async def payment_handler(
    callback: CallbackQuery,
    callback_data: SubscriptionCallbackFactory,
    settings: Settings,
):
    await callback.answer()
    match callback_data.plan:
        case SubscriptionPlan.ONE_MONTH_SUBSCRIPTION:
            description = "Длительность: 1 месяц"
            prices = [
                LabeledPrice(label="Подписка на 1 месяц", amount=490 * 100),
            ]
        case SubscriptionPlan.ONE_YEAR_SUBSCRIPTION:
            description = "Длительность: 1 год"
            prices = [
                LabeledPrice(label="Подписка на 1 год", amount=3900 * 100),
            ]
        case _:
            assert False, 'Unexpected subscription plan'
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Оплата подписки",
        description=description,
        payload=callback_data.plan,
        provider_token=settings.bot.PROVIDER_TOKEN.get_secret_value(),
        start_parameter="test",
        currency="RUB",
        prices=prices
    )


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message,
    user: User,
    settings: Settings,
    db_session: AsyncSession,
):
    payload = message.successful_payment.invoice_payload
    await message.answer(
        text='Ваша подписка активирована! Приятного пользования!',
        # reply_markup=connect_vpn_kb(active=True),
    )
    logger.info(f"Successful payment for user {user.username}: {message.successful_payment.invoice_payload}")
