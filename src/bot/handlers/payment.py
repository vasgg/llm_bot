from logging import getLogger

from aiogram import F, Router
from aiogram.types import CallbackQuery, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.controllers.payments import add_payment_to_db, get_subscription_payment
from bot.internal.callbacks import PaidEntityCallbackFactory
from bot.internal.enums import PaidEntity
from bot.internal.keyboards import autopayment_cancelled_kb, payment_link_kb
from bot.internal.lexicon import payment_text
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
    db_session: AsyncSession,
):
    await callback.answer()
    match callback_data.entity:
        case PaidEntity.ONE_MONTH_SUBSCRIPTION:
            description = "Оплата подписки, длительность: 1 месяц."
            amount = 390
        case PaidEntity.ONE_YEAR_SUBSCRIPTION:
            description = "Оплата подписки, длительность: 1 год."
            amount = 3900
        case PaidEntity.PICTURES_COUNTER_REFRESH:
            description = "Сброс лимита картинок."
            amount = 150
        case _:
            assert False, "Unexpected paid entity"
    payment = await get_subscription_payment(amount, description, callback.from_user.id, callback_data.entity)
    confirmation_url = payment.confirmation.confirmation_url
    await add_payment_to_db(payment.id, amount, description, callback.from_user.id, db_session)
    await callback.message.answer(
        text=payment_text["payment_url_text"].format(description=description),
        reply_markup=payment_link_kb(amount, confirmation_url),
    )


@router.callback_query(F.data == "cancel_autopayment")
async def cancel_payment_dialog(callback: CallbackQuery, user: User):
    await callback.answer()
    date = user.expired_at.strftime("%d.%m.%Y")
    await callback.message.answer(
        text=payment_text["cancel_payment"].format(date=date),
        reply_markup=autopayment_cancelled_kb(),
    )


@router.callback_query(F.data == "autopayment_cancelled")
async def cancel_payment_handler(callback: CallbackQuery, user: User):
    await callback.answer()
    date = user.expired_at.strftime("%d.%m.%Y")
    user.is_autopayment_enabled = False
    user.subscription_duration = None
    await callback.message.edit_text(
        text=payment_text["payment_cancelled"].format(date=date),
    )
