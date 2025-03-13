import logging

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self, token: str, assistant_id: str):
        self.client = AsyncOpenAI(api_key=token)
        self.assistant_id = assistant_id

    async def delete_thread(self, thread_id: str):
        await self.client.beta.threads.delete(thread_id)

    async def new_thread(self, initial_message: str | None = None) -> str:
        thread = await self.client.beta.threads.create()
        logging.debug(f"Created new thread {thread.id}")

        if initial_message:
            await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=initial_message)
            logging.debug(f"Initial context added to thread {thread.id}")

        return thread.id

    async def get_response(self, ai_thread_id: str, text: str) -> str | None:
        await self.client.beta.threads.messages.create(thread_id=ai_thread_id, role="user", content=text)
        run = await self.client.beta.threads.runs.create_and_poll(
            thread_id=ai_thread_id, assistant_id=self.assistant_id
        )
        logger.info(f"Run completed: {run.status=}")
        if run.status == "completed":
            messages = await self.client.beta.threads.messages.list(thread_id=ai_thread_id)
            return messages.data[0].content[0].text.value

        return None
