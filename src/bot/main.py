import logging
from asyncio import create_task, run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.ai_client import AIClient
from bot.config import Settings
from bot.handlers.base import router as base_router
from bot.handlers.ai import router as media_router
from bot.handlers.payment import router as payment_router
from bot.internal.config_dicts import setup_logs
from bot.internal.notify_admin import on_shutdown, on_startup
from bot.middlewares.auth_middleware import AuthMiddleware
from bot.middlewares.logging_middleware import LoggingMiddleware
from bot.middlewares.session_middleware import DBSessionMiddleware
from bot.middlewares.updates_dumper_middleware import UpdatesDumperMiddleware
from database.database_connector import get_db


async def main():
    setup_logs("suslik_robot")
    settings = Settings()
    storage = MemoryStorage()

    bot = Bot(
        token=settings.bot.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    openai_client = AIClient(
        token=settings.gpt.OPENAI_API_KEY.get_secret_value(), assistant_id=settings.gpt.ASSISTANT_ID.get_secret_value()
    )

    dispatcher = Dispatcher(storage=storage, settings=settings, openai_client=openai_client)

    db = get_db(settings)
    db_session_middleware = DBSessionMiddleware(db)

    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    # dispatcher.startup.register(set_bot_commands)
    dispatcher.message.middleware(db_session_middleware)
    dispatcher.callback_query.middleware(db_session_middleware)
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.message.middleware.register(LoggingMiddleware())
    dispatcher.callback_query.middleware.register(LoggingMiddleware())
    dispatcher.include_routers(
        payment_router,
        base_router,
        media_router,
    )

    logging.info("suslik robot started")
    await dispatcher.start_polling(bot, skip_updates=True)


def run_main():
    run(main())


if __name__ == "__main__":
    run_main()
