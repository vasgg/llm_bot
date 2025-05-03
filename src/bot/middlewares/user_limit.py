from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware

from bot.config import settings
from bot.internal.lexicon import replies
from database.models import User


class UserLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = settings.bot.USERS_THRESHOLD):
        self.limit = limit

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("user")
        if not user:
            return await handler(event, data)

        if user.id <= self.limit or user.tg_id in settings.bot.ADMINS:
            return await handler(event, data)
        else:
            await event.answer(replies["users_limit_exceeded"])
            return None
