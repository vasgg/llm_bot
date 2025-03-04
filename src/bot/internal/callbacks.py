from aiogram.filters.callback_data import CallbackData

from src.bot.internal.enums import SpaceType, SubscriptionPlan


class SubscriptionCallbackFactory(CallbackData, prefix="subscription"):
    plan: SubscriptionPlan


class SpaceCallbackFactory(CallbackData, prefix="space"):
    choice: SpaceType
