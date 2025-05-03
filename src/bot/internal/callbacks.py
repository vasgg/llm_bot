from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import MenuButtons, PaidEntity


class PaidEntityCallbackFactory(CallbackData, prefix="paid_functions"):
    entity: PaidEntity


class NewDialogCallbackFactory(CallbackData, prefix="new_dialog"):
    choice: MenuButtons
