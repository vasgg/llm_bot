from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import NewDialogCallbackFactory
from bot.internal.enums import MenuButtons


def new_dialog_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Да", NewDialogCallbackFactory(choice=MenuButtons.YES).pack()),
        ("Нет", NewDialogCallbackFactory(choice=MenuButtons.NO).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
