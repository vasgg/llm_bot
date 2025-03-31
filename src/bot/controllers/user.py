import logging

from aiogram.types import User
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.lexicon import ORDER, QUESTIONS
from database.models import User as BotUser

logger = logging.getLogger(__name__)


async def add_user_to_db(user, db_session: AsyncSession) -> BotUser:
    new_user = BotUser(tg_id=user.id, fullname=user.full_name, username=compose_username(user))
    db_session.add(new_user)
    await db_session.flush()
    logger.info(f"New user created: {new_user}")
    return new_user


async def get_user_from_db_by_tg_id(telegram_id: int, db_session: AsyncSession) -> BotUser | None:
    query = select(BotUser).filter(BotUser.tg_id == telegram_id)
    result: Result = await db_session.execute(query)
    return result.scalar_one_or_none()


# async def update_db_user_expiration(user: User, duration: relativedelta, db_session: AsyncSession):
#     current_time = datetime.now(UTC)
#     if user.expired_at > current_time:
#         user.expired_at += duration
#     else:
#         user.expired_at = current_time + duration
#     db_session.add(user)
#     logger.info(f"Subscription for {user.tg_id} prolonged to {user.expired_at}")
#     return user.expired_at


def compose_username(user: User):
    return "@" + user.username if user.username else user.full_name.replace(" ", "_")


def is_ready(user: User) -> bool:
    return all(getattr(user, field) is not None for field in QUESTIONS)


async def ask_next_question(user: User, index: int) -> tuple:
    for field in ORDER:
        if getattr(user, field) is None:
            question = QUESTIONS[field][index]
            return field, question
    return None, None


def generate_user_context(user: BotUser) -> str:
    return (
        "Контекст пользователя:\n"
        f"- Имя пользователя: {user.fullname}\n"
        f"- Тип участка: {user.space or 'не указано'}\n"
        f"- Бюджет: {user.budget or 'не указано'}\n"
        f"- Местоположение: {user.geography or 'не указано'}\n"
        f"- Стиль: {user.style or 'не указан'}\n"
    )
