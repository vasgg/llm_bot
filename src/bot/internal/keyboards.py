from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import SubscriptionCallbackFactory
from bot.internal.enums import SubscriptionPlan


def subscription_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Месяц", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_MONTH_SUBSCRIPTION).pack()),
        ("Годовая подписка", SubscriptionCallbackFactory(plan=SubscriptionPlan.ONE_YEAR_SUBSCRIPTION).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()



def unsubscription_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Отмена подписки', callback_data='unsubscribe')
    return kb.as_markup()