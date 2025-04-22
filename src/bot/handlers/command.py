from asyncio import sleep
from datetime import UTC
from logging import getLogger
from random import randint

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings
from bot.controllers.bot import imitate_typing
from bot.controllers.user import ask_next_question
from bot.internal.enums import SubscriptionStatus, Form, AIState
from bot.internal.lexicon import replies
from database.models import User


router = Router()
logger = getLogger(__name__)


@router.message(Command("start", "support"))
async def command_handler(
    message: Message,
    command: CommandObject,
    user: User,
    settings: Settings,
    state: FSMContext,
    db_session: AsyncSession,
) -> None:
    match command.command:
        case "start":
            start_file_path = "src/bot/data/start.png"
            await message.answer_photo(
                FSInputFile(path=start_file_path),
            )
            async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
                if not user.is_context_added:
                    await sleep(1)
                    await message.answer(replies[0].format(fullname=user.fullname))
                    random_index = randint(0, 9)
                    await state.update_data(question_index=random_index)
                    await imitate_typing()
                    field, question = await ask_next_question(user, random_index)
                    await state.set_state(getattr(Form, field))
                    await message.answer(question)
                else:
                    await sleep(1)
                    await message.answer(replies[1].format(fullname=user.fullname))
                    # user.is_context_added = True
                    # db_session.add(user)
                    # await db_session.flush()
                    await imitate_typing()
                    await state.set_state(AIState.IN_AI_DIALOG)
        case "support":
            if user.is_subscribed:
                ...
            else:
                ...
        case _:
            assert False, "Unexpected command"
