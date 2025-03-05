import logging

from aiogram.types import User
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.internal.dicts import texts
from src.bot.internal.enums import SpaceType
from src.database.models import User as BotUser

logger = logging.getLogger(__name__)


async def add_user_to_db(user, db_session: AsyncSession) -> BotUser:
    new_user = BotUser(
        tg_id=user.id, fullname=user.full_name, username=compose_username(user)
    )
    db_session.add(new_user)
    await db_session.flush()
    logger.info(f"New user created: {new_user}")
    return new_user


async def get_user_from_db_by_tg_id(
    telegram_id: int, db_session: AsyncSession
) -> BotUser | None:
    query = select(BotUser).filter(BotUser.tg_id == telegram_id)
    result: Result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    return user


# async def update_db_user_expiration(user: User, duration: relativedelta, db_session: AsyncSession):
#     current_time = datetime.now(UTC)
#     if user.expired_at > current_time:
#         user.expired_at += duration
#     else:
#         user.expired_at = current_time + duration
#     db_session.add(user)
#     logger.info(f"Subscription for {user.tg_id} prolonged to {user.expired_at}")
#     return user.expired_at


def get_missing_fields(user: BotUser):
    missing = {}
    if user.budget is None:
        missing["budget"] = (
            texts["indoor_budget"]
            if user.space_type == SpaceType.INDOOR
            else texts["outdoor_budget"]
        )
    if user.geography is None:
        missing["geography"] = (
            texts["indoor_budget"]
            if user.space_type == SpaceType.INDOOR
            else texts["outdoor_budget"]
        )
    if user.style is None:
        missing["style"] = (
            texts["indoor_style"]
            if user.space_type == SpaceType.INDOOR
            else texts["outdoor_style"]
        )
    if user.interests is None:
        missing["interests"] = (
            texts["indoor_interests"]
            if user.space_type == SpaceType.INDOOR
            else texts["outdoor_interests"]
        )
    return missing


def compose_username(user: User):
    return "@" + user.username if user.username else user.full_name.replace(" ", "_")
