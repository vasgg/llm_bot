from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import NewDialogCallbackFactory
from bot.internal.enums import MenuButtons


def new_dialog_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ('"Суслик лайт"  Ежемесячно: 490₽', NewDialogCallbackFactory(choice=MenuButtons.YES).pack()),
        ('"Суслик PRO: год заботы 💚" Годовая подписка: 3900₽ (со скидкой 17%!)', NewDialogCallbackFactory(choice=MenuButtons.NO).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
