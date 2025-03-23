import logging

from openai import AsyncOpenAI, BadRequestError

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

    async def get_response_with_image(self, thread_id: str, text: str, image_bytes: bytes) -> str | None:
        try:
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

            run = await self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id, assistant_id=self.assistant_id
            )

            if run.status == "completed":
                messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                return messages.data[0].content[0].text.value
            else:
                return None

        except BadRequestError as e:
            logging.exception(f"OpenAI API Error: {e}")
            if e.status_code == 429:
                return "Превышены лимиты запросов. Пожалуйста, попробуйте позже."
            return "Ошибка при обработке изображения. Убедитесь, что файл корректного формата."
