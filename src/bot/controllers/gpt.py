import logging

from openai import AsyncOpenAI, OpenAIError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.ai_client import AIClient
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


async def get_or_create_ai_thread(
    user: User,
    openai_client: AIClient,
    db_session: AsyncSession,
) -> str:
    if user.ai_thread:
        return user.ai_thread

    thread_id = await openai_client.new_thread()
    user.ai_thread = thread_id
    db_session.add(user)
    await db_session.flush()
    return thread_id


async def update_existing_assistant_prompt(
    client: AsyncOpenAI,
    assistant_id: str,
) -> None:
    try:
        with open(PROMPT_FILE, encoding="utf-8") as file:
            prompt = file.read()

        await client.beta.assistants.update(assistant_id=assistant_id, instructions=prompt)

        print(f"Промпт успешно обновлён у ассистента {assistant_id}")

    except FileNotFoundError:
        print(f"Файл '{PROMPT_FILE}' не найден.")
    except OpenAIError as e:
        print(f"Ошибка OpenAI API: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


async def update_existing_assistant_model(
    client: AsyncOpenAI,
    assistant_id: str,
    model: str,
) -> None:
    try:
        await client.beta.assistants.update(assistant_id=assistant_id, model=model)
        print(f"Модель успешно обновлена у ассистента {assistant_id}")
    except OpenAIError as e:
        print(f"Ошибка OpenAI API: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
