import logging

from openai import AsyncOpenAI, OpenAIError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.ai_client import AIClient
from bot.controllers.user import generate_user_context
from database.models import User

logger = logging.getLogger(__name__)
PROMPT_FILE = "src/bot/data/prompt.md"


async def create_openai_assistant(client: AsyncOpenAI):
    try:
        async with open(PROMPT_FILE, encoding="utf-8") as file:
            instructions = file.read()

        response = await client.beta.assistants.create(
            name="suslik_ai_landscape_designer",
            instructions=instructions,
            tools=[{"type": "file_search"}],
            model="gpt-4-turbo",
        )
        return response.id

    except FileNotFoundError:
        logger.info(f"Ошибка: Файл '{PROMPT_FILE}' не найден.")
    except OpenAIError as e:
        logger.info(f"Ошибка API OpenAI: {e}")
    except Exception as e:
        logger.info(f"Непредвиденная ошибка: {e}")


async def check_ai_thread(user: User, openai_client: AIClient, db_session: AsyncSession) -> str:
    thread_id = user.ai_tread
    if thread_id is None:
        context = generate_user_context(user)
        thread_id = await openai_client.new_thread(initial_message=context)
        user.ai_tread = thread_id
        db_session.add(user)
        await db_session.flush()
    return thread_id
