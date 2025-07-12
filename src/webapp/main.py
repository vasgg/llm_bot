from contextlib import asynccontextmanager

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from fastapi import FastAPI
import uvicorn
from starlette.datastructures import State
from bot.config import get_settings
from database.database_connector import get_db
from routers.webhook import router as webhook_router
from bot.internal.helpers import setup_logs


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = AiohttpSession()
    settings = get_settings()
    db = get_db(settings)
    bot = Bot(
        token=settings.bot.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
    me = await bot.get_me()
    app.state.bot_id = me.id
    app.state.bot = bot
    app.state.settings = settings
    app.state.db = db
    yield
    await db.dispose()
    await session.close()


app = FastAPI(lifespan=lifespan)
app.state: State  # type: ignore


setup_logs("yookassa_webhook")

app.include_router(webhook_router, prefix="/webhook")

if __name__ == "__main__":
    uvicorn.run("src.webapp.main:app", host="0.0.0.0", port=8080, reload=True)
