from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import PaidEntityCallbackFactory
from bot.internal.enums import PaidEntity


def subscription_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Месяц", PaidEntityCallbackFactory(entity=PaidEntity.ONE_MONTH_SUBSCRIPTION).pack()),
        ("Годовая подписка", PaidEntityCallbackFactory(entity=PaidEntity.ONE_YEAR_SUBSCRIPTION).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def refresh_pictures_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Купить доп. пакет",
        callback_data=PaidEntityCallbackFactory(entity=PaidEntity.PICTURES_COUNTER_REFRESH).pack(),
    )
    return kb.as_markup()
