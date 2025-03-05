from asyncio import run
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import Settings
from bot.middlewares.auth_middleware import AuthMiddleware
from bot.middlewares.logging_middleware import LoggingMiddleware
from database.database_connector import get_db
from bot.internal.commands import set_bot_commands
from bot.internal.notify_admin import on_shutdown, on_startup
from bot.middlewares.session_middleware import DBSessionMiddleware
from bot.middlewares.updates_dumper_middleware import UpdatesDumperMiddleware
from bot.handlers.main_handlers import router as main_router
from bot.internal.config_dicts import setup_logs


async def main():
    setup_logs("suslik_robot")
    settings = Settings()
    storage = MemoryStorage()

    bot = Bot(
        token=settings.bot.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dispatcher = Dispatcher(storage=storage, settings=settings)

    db = get_db(settings)
    db_session_middleware = DBSessionMiddleware(db)

    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.startup.register(set_bot_commands)
    dispatcher.message.middleware(db_session_middleware)
    dispatcher.callback_query.middleware(db_session_middleware)
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.message.middleware.register(LoggingMiddleware())
    dispatcher.callback_query.middleware.register(LoggingMiddleware())
    dispatcher.include_routers(
        main_router,
    )

    logging.info("suslik robot started")
    await dispatcher.start_polling(bot)


def run_main():
    run(main())


if __name__ == "__main__":
    run_main()
