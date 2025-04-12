from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import SubscriptionPlan


class SubscriptionCallbackFactory(CallbackData, prefix="subscription"):
    plan: SubscriptionPlan
