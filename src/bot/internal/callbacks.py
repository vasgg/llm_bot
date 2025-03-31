from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import MenuButtons, SubscriptionPlan


class SubscriptionCallbackFactory(CallbackData, prefix="subscription"):
    plan: SubscriptionPlan


class NewDialogCallbackFactory(CallbackData, prefix="new_dialog"):
    choice: MenuButtons
