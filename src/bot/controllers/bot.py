from asyncio import sleep
import logging
from datetime import datetime, timezone
from random import randint
import re
from aiogram import Bot
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from aiogram.enums import ParseMode

from bot.config import Settings
from bot.internal.consts import ONE_DAY, MAX_MESSAGE_LENGTH
from database.database_connector import DatabaseConnector

logger = logging.getLogger(__name__)


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(r"([%s])" % re.escape(escape_chars), r"\\\1", text)


def escape_stars(s):
    process = s.split("**")
    return "*".join([escape_markdown_v2(i) for i in process])


def extract_content(messages: list[dict[str, str]]) -> str:
    return " ".join(message["content"] for message in messages)


def starts_with_hash_space(s: str) -> bool:
    pattern = r"^#+\s"
    return bool(re.match(pattern, s))


def refactor_string(string: str) -> str:
    lines = string.splitlines()
    indices_to_wrap = []

    for i, line in enumerate(lines):
        if starts_with_hash_space(line):
            lines[i] = re.sub(r"^#+\s", "", line)
            indices_to_wrap.append(i)
        lines[i] = escape_stars(lines[i])

    for i in indices_to_wrap:
        lines[i] = f"*{lines[i]}*"

    return "\n".join(lines)


async def imitate_typing(delay_from=1, delay_to=3):
    await sleep(randint(delay_from, delay_to))


async def truncate_user_limit_table(db_session: AsyncSession) -> None:
    await db_session.execute(text("TRUNCATE TABLE user_limits RESTART IDENTITY"))


def get_seconds_until_starting_mark(settings: Settings, current_hour, utcnow):
    if current_hour >= settings.bot.UTC_STARTING_MARK:
        hours_to_sleep = 24 - current_hour + settings.bot.UTC_STARTING_MARK
    else:
        hours_to_sleep = settings.bot.UTC_STARTING_MARK - current_hour
    seconds_to_sleep = hours_to_sleep * 3600 - utcnow.minute * 60 - utcnow.second
    return seconds_to_sleep


async def daily_routine(
    bot: Bot,
    settings: Settings,
    db_connector: DatabaseConnector,
):
    utcnow = datetime.now(timezone.utc)
    current_hour = utcnow.hour
    seconds_to_sleep = get_seconds_until_starting_mark(settings, current_hour, utcnow)
    await sleep(seconds_to_sleep)
    while True:
        async with db_connector.session_factory() as session:
            await truncate_user_limit_table(session)
            # for user in await get_all_users_with_active_subscription(session):
            #     utcnow = datetime.now(timezone.utc)
            #     delta = utcnow.date() - user.expired_at
            #     if delta.days == 1:
            #         await bot.send_message(
            #             chat_id=user.telegram_id,
            #             text=await get_text_by_prompt(prompt='subscribtion_almost_over', db_session=session),
            #             reply_markup=get_premium_keyboard(),
            #         )
            #         logger.info(f"{'ending subscription reminder was sent to ' + str(user)}")
            #
            #     elif delta.days == 0:
            #         user.subscription_status = UserSubscriptionType.ACCESS_EXPIRED
            #         await bot.send_message(
            #             chat_id=user.telegram_id,
            #             text=await get_text_by_prompt(prompt='subscribtion_over', db_session=session),
            #             reply_markup=get_premium_keyboard(),
            #         )
            #         logger.info(f"{'ending subscription notification was sent to ' + str(user)}")
            await session.commit()
        await sleep(ONE_DAY)

def validate_message_length(
    message: Message,
) -> bool:
    raw_text = message.text or message.caption

    if len(raw_text) > MAX_MESSAGE_LENGTH:
        return False

    return True