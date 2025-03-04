from enum import StrEnum, auto


class SubscriptionPlan(StrEnum):
    ONE_WEEK_DEMO_ACCESS = auto()
    ONE_MONTH_SUBSCRIPTION = auto()
    SIX_MONTH_SUBSCRIPTION = auto()
    ONE_YEAR_SUBSCRIPTION = auto()


class Stage(StrEnum):
    DEV = auto()
    PROD = auto()


class SubscriptionStatus(StrEnum):
    INACTIVE = auto()
    ACTIVE = auto()
    CREATED = auto()
    RENEWED = auto()
    PROLONGED = auto()


class SpaceType(StrEnum):
    INDOOR = auto()
    OUTDOOR = auto()
