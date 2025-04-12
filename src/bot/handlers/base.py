from asyncio import sleep
from logging import getLogger
from random import choice, randint

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy.ext.asyncio import AsyncSession

from bot.ai_client import AIClient
from bot.config import Settings
from bot.controllers.bot import imitate_typing, refactor_string
from bot.controllers.gpt import get_or_create_ai_thread
from bot.controllers.user import ask_next_question, generate_user_context
from bot.controllers.voice import extract_text_from_message
from bot.internal.enums import AIState, Form
from bot.internal.lexicon import ORDER, REACTIONS, replies
from database.models import User

router = Router()
logger = getLogger(__name__)


@router.message(CommandStart())
async def command_handler(
    message: Message,
    user: User,
    state: FSMContext,
) -> None:
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


@router.message(StateFilter(Form), F.text | F.voice)
async def form_handler(
    message: Message, user: User, state: FSMContext, db_session: AsyncSession, openai_client: AIClient
):
    current_state = await state.get_state()
    field = current_state.split(":")[-1]

    user_answer = await extract_text_from_message(message, openai_client)
    if not user_answer:
        return

    setattr(user, field, user_answer)
    db_session.add(user)
    await db_session.flush()
    data = await state.get_data()
    question_index = data.get("question_index", choice(list(REACTIONS[field].keys())))
    reaction = REACTIONS[field][question_index].format(**{field: user_answer})

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await imitate_typing()
        await message.answer(reaction)
        await imitate_typing()

        if all(getattr(user, f) for f in ORDER):
            await state.clear()
            user_context = generate_user_context(user)
            # if not user.ai_thread:
            #     await openai_client.apply_context_to_thread(user, user_context, db_session)
            # else:
            await openai_client.apply_context_to_thread(user, user_context, db_session, use_existing_thread=True)
            await message.answer(replies[3])
            await state.set_state(AIState.IN_AI_DIALOG)
        else:
            next_field, next_question = await ask_next_question(user, question_index)
            await state.set_state(getattr(Form, next_field))
            await state.update_data(question_index=question_index)
            await imitate_typing()
            await message.answer(next_question)


# @router.message(Command("settings"))
# async def command_settings_handler(
#     message: Message,
#     user: User,
#     state: FSMContext,
# ) -> None:
#     if user.is_context_added:
#         await message.answer('[вот тут нужен правильный текст] Чтобы добавить настройки в контекст диалога, нужно пройти короткий опрос. Начать опрос?',
#                              reply_markup=new_dialog_kb())
#     else:
#         start_file_path = "src/bot/data/start.png"
#         await message.answer_photo(
#             FSInputFile(path=start_file_path),
#         )
#         async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
#             await sleep(1)
#             await message.answer(replies[1])
#             await imitate_typing()
#
#             field, question = await ask_next_question(user, randint(0, 9))
#             await state.set_state(getattr(Form, field))
#             await message.answer(question)


@router.message(AIState.IN_AI_DIALOG, F.text)
async def ai_assistant_text_handler(
    message: Message, openai_client: AIClient, user: User, settings: Settings, db_session: AsyncSession
):
    thread_id = await get_or_create_ai_thread(user, openai_client, db_session)
    await message.forward(settings.bot.CHAT_LOG_ID)

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        response = await openai_client.get_response(thread_id, message.text, message, user.fullname)
        if response is None:
            # await message.answer("Извините, я отвлекся, давайте начнём новый разговор.")
            return

        cleaned_response = refactor_string(response)
        msg_answer = await message.answer(cleaned_response, parse_mode=ParseMode.MARKDOWN_V2)
        await msg_answer.forward(settings.bot.CHAT_LOG_ID)


# @router.callback_query(NewDialogCallbackFactory.filter())
# async def dialog_handler(
#     callback: CallbackQuery,
#     callback_data: NewDialogCallbackFactory,
#     state: FSMContext,
#     user: User,
#     db_session: AsyncSession,
# ) -> None:
#     await callback.answer()
#     match callback_data.choice:
#         case MenuButtons.YES:
#             await callback.message.delete()
#             await state.clear()
#             user.is_context_added = False
#             user.ai_thread = None
#             user.budget = None
#             user.space = None
#             user.geography = None
#             user.style = None
#             db_session.add(user)
#             await db_session.flush()
#             start_file_path = "src/bot/data/start.png"
#             await callback.message.answer_photo(
#                 FSInputFile(path=start_file_path),
#             )
#             async with ChatActionSender.typing(bot=callback.message.bot, chat_id=callback.message.chat.id):
#                 await sleep(1)
#                 await callback.message.answer(replies[1])
#                 await sleep(1)
#                 field, question = await ask_next_question(user, randint(0, 9))
#                 await state.set_state(getattr(Form, field))
#                 await callback.message.answer(question)
#         case MenuButtons.NO:
#             await callback.message.delete()
