from aiogram.types import InlineKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import PaidEntityCallbackFactory
from bot.internal.enums import PaidEntity


def subscription_kb(prolong: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    month_text = "Продлить на месяц" if prolong else "Месяц"
    year_text = "Продлить на год" if prolong else "Годовая подписка"
    for text, callback in [
        (month_text, PaidEntityCallbackFactory(entity=PaidEntity.ONE_MONTH_SUBSCRIPTION).pack()),
        (year_text, PaidEntityCallbackFactory(entity=PaidEntity.ONE_YEAR_SUBSCRIPTION).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def payment_link_kb(value: int, url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=f"Оплатить {value}₽", url=url)
    return kb.as_markup()


def cancel_autopayment_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Отменить автопродление", callback_data="cancel_autopayment")
    return kb.as_markup()


def refresh_pictures_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Купить доп. пакет",
        callback_data=PaidEntityCallbackFactory(entity=PaidEntity.PICTURES_COUNTER_REFRESH).pack(),
    )
    return kb.as_markup()


contact_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Выберите контакт", request_users=KeyboardButtonRequestUsers(request_id=1))]],
    resize_keyboard=True,
    one_time_keyboard=True,
)
