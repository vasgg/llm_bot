from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.callbacks import SpaceCallbackFactory
from bot.internal.enums import SpaceType


def choose_space_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Помещение", SpaceCallbackFactory(choice=SpaceType.INDOOR).pack()),
        ("Участок", SpaceCallbackFactory(choice=SpaceType.OUTDOOR).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
