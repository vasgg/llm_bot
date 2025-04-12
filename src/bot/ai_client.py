from asyncio import get_event_loop, sleep
import logging

from aiogram.types import Message
from openai import AsyncOpenAI, BadRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.lexicon import replies
from database.models import User

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self, token: str, assistant_id: str):
        self.client = AsyncOpenAI(api_key=token)
        self.assistant_id = assistant_id

    async def delete_thread(self, thread_id: str):
        await self.client.beta.threads.delete(thread_id)

    async def new_thread(self) -> str:
        thread = await self.client.beta.threads.create()
        logging.debug(f"Created new thread {thread.id}")
        return thread.id

    async def get_response(self, ai_thread_id: str, text: str, message: Message, fullname: str) -> str | None:
        runs = await self.client.beta.threads.runs.list(thread_id=ai_thread_id, limit=1)
        if runs.data and runs.data[0].status in ("queued", "in_progress"):
            logger.info(f"Waiting for active run {runs.data[0].id} in thread {ai_thread_id}")
            await message.answer(replies[4].format(fullname=fullname))
            await self.wait_for_run_completion(ai_thread_id, runs.data[0].id)

        await self.client.beta.threads.messages.create(thread_id=ai_thread_id, role="user", content=text)
        run = await self.client.beta.threads.runs.create(thread_id=ai_thread_id, assistant_id=self.assistant_id)
        run = await self.wait_for_run_completion(ai_thread_id, run.id)

        if run.status == "completed":
            messages = await self.client.beta.threads.messages.list(thread_id=ai_thread_id)
            return messages.data[0].content[0].text.value
        return None

    async def get_response_with_image(
        self, thread_id: str, text: str, image_bytes: bytes, message: Message, fullname: str
    ) -> str | None:
        try:
            runs = await self.client.beta.threads.runs.list(thread_id=thread_id, limit=1)
            if runs.data and runs.data[0].status in ("queued", "in_progress"):
                logger.info(f"Waiting for active run {runs.data[0].id} in thread {thread_id}")
                await message.answer(replies[4].format(fullname=fullname))
                await self.wait_for_run_completion(thread_id, runs.data[0].id)

            uploaded_file = await self.client.files.create(
                file=("image.png", image_bytes, "image/png"), purpose="assistants"
            )

            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=[
                    {"type": "text", "text": text},
                    {"type": "image_file", "image_file": {"file_id": uploaded_file.id}},
                ],
            )

            run = await self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=self.assistant_id)
            run = await self.wait_for_run_completion(thread_id, run.id)

            if run.status == "completed":
                messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                return messages.data[0].content[0].text.value
            return None

        except BadRequestError as e:
            logger.exception(f"OpenAI API Error: {e}")
            if e.status_code == 429:
                return "Превышены лимиты запросов. Пожалуйста, попробуйте позже."
            return "Ошибка при обработке изображения. Убедитесь, что файл корректного формата."

    async def apply_context_to_thread(
        self, user: User, context: str, db_session: AsyncSession, use_existing_thread: bool = False
    ) -> str:
        if use_existing_thread and user.ai_thread:
            thread_id = user.ai_thread
            await self.client.beta.threads.messages.create(thread_id=thread_id, role="user", content=context)
        else:
            thread = await self.client.beta.threads.create()
            thread_id = thread.id
            await self.client.beta.threads.messages.create(thread_id=thread_id, role="user", content=context)
            user.ai_thread = thread_id

        user.is_context_added = True
        db_session.add(user)
        await db_session.flush()
        logger.info(f"Added context to thread {thread_id}")
        return thread_id

    async def wait_for_run_completion(self, thread_id: str, run_id: str, interval: int = 2, timeout: int = 120):
        start = get_event_loop().time()
        while True:
            run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status in ("completed", "failed", "cancelled", "expired"):
                return run
            if get_event_loop().time() - start > timeout:
                raise TimeoutError(f"Run {run_id} in thread {thread_id} did not finish in time")
            await sleep(interval)
