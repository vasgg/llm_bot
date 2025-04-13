from logging import getLogger

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from openai import BadRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.ai_client import AIClient
from bot.config import Settings
from bot.controllers.bot import refactor_string
from bot.controllers.gpt import get_or_create_ai_thread
from bot.controllers.voice import process_voice
from bot.internal.enums import AIState
from database.models import User

router = Router()
logger = getLogger(__name__)


@router.message(AIState.IN_AI_DIALOG, F.voice)
async def ai_assistant_voice_handler(
    message: Message, openai_client: AIClient, user: User, settings: Settings, db_session: AsyncSession
):
    thread_id = await get_or_create_ai_thread(user, openai_client, db_session)
    await message.forward(settings.bot.CHAT_LOG_ID)
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        transcription = await process_voice(message, openai_client)
        response = await openai_client.get_response(thread_id, transcription, message, user.fullname)
        if response is None:
            # await message.answer("Извините, я отвлекся, давайте начнём новый разговор.")
            return
        cleaned_response = refactor_string(response)
        msg_answer = await message.answer(cleaned_response, parse_mode=ParseMode.MARKDOWN_V2)
        await msg_answer.forward(settings.bot.CHAT_LOG_ID)


@router.message(AIState.IN_AI_DIALOG, F.photo)
async def ai_assistant_photo_handler(
    message: Message, openai_client: AIClient, user: User, settings: Settings, db_session: AsyncSession
):
    if message.media_group_id is not None:
        await message.answer(
            "Пожалуйста, отправляйте только по одному изображению за раз, чтобы я мог корректно ответить."
        )
        return

    thread_id = await get_or_create_ai_thread(user, openai_client, db_session)
    await message.forward(settings.bot.CHAT_LOG_ID)

    user_text = message.caption or "Пользователь отправил изображение без дополнительного текста."

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        try:
            photo = message.photo[-1]
            file_info = await message.bot.get_file(photo.file_id)

            file_bytes = await message.bot.download_file(file_info.file_path)
            image_bytes = file_bytes.read()

            prompt_text = (
                f"{user_text}\n\nОпиши, что на изображении, и ответь пользователю с учётом текущего контекста диалога."
            )

            response = await openai_client.get_response_with_image(
                thread_id=thread_id,
                text=prompt_text,
                image_bytes=image_bytes,
                message=message,
                fullname=user.fullname,
            )

            if response is None:
                # await message.answer("Извините, я отвлекся, давайте начнём новый разговор.")
                return

            cleaned_response = refactor_string(response)
            msg_answer = await message.answer(cleaned_response, parse_mode=ParseMode.MARKDOWN_V2)
            await msg_answer.forward(settings.bot.CHAT_LOG_ID)

        except BadRequestError as e:
            logger.error(f"OpenAI API Error: {e}")
            if e.status_code == 429:
                await message.answer("Превышены лимиты запросов. Пожалуйста, попробуйте позже.")
            else:
                await message.answer(
                    "Ошибка при обработке изображения. "
                    "Убедитесь, что изображение корректного формата (jpg, png) и попробуйте снова."
                )
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            await message.answer("Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")
