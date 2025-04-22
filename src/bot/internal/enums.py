from enum import StrEnum, auto

from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    space = State()
    geography = State()
    request = State()


class AIState(StatesGroup):
    IN_AI_DIALOG = State()


class SubscriptionPlan(StrEnum):
    ONE_MONTH_SUBSCRIPTION = auto()
    ONE_YEAR_SUBSCRIPTION = auto()


class MenuButtons(StrEnum):
    YES = auto()
    NO = auto()


class SubscriptionStatus(StrEnum):
    INACTIVE = auto()
    ACTIVE = auto()
    CREATED = auto()
    RENEWED = auto()
    PROLONGED = auto()
