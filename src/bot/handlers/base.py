import io
from asyncio import sleep
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
from bot.controllers.bot import refactor_string
from bot.controllers.gpt import check_ai_thread
from bot.controllers.user import ask_next_question, is_ready
from bot.controllers.voice import convert_to_mp3
from bot.internal import lexicon
from bot.internal.enums import AIState, Form
from bot.internal.lexicon import ORDER, REACTIONS, greetings
from database.models import User

router = Router()


# @router.message(F.photo)
# async def handle_photo_info(message: Message, settings: Settings):
#     if message.from_user.id not in settings.bot.ADMINS:
#         return
#     file_name = (message.photo[-1].file_id,)
#     await message.answer(f"<b>File ID:</b> {file_name[0]}")


@router.message(CommandStart())
async def command_handler(
    message: Message,
    user: User,
    state: FSMContext,
    is_new_user: bool,
    db_session: AsyncSession,
) -> None:
    random_index = randint(0, 9)
    if is_new_user:
        current_file_path = "src/bot/data/start.png"
        await message.answer_photo(
            FSInputFile(path=current_file_path),
            caption=greetings[0],
        )
        await sleep(randint(1, 3))

    if is_ready(user):
        if not user.is_intro_shown:
            await message.answer(
                lexicon.results[random_index].format(
                    space=user.space,
                    budget=user.budget,
                    geography=user.geography,
                    style=user.style,
                )
            )
            user.is_intro_shown = True
            db_session.add(user)
            await db_session.flush()
            await sleep(randint(1, 3))

        await message.answer(greetings[1])
        await state.set_state(AIState.IN_AI_DIALOG)

    else:
        field, question = await ask_next_question(user, random_index)
        await state.set_state(getattr(Form, field))
        await message.answer(question)


@router.message(StateFilter(Form), F.text)
async def form_handler(message: Message, user: User, state: FSMContext, db_session: AsyncSession):
    current_state = await state.get_state()
    field = current_state.split(":")[-1]

    setattr(user, field, message.text)
    db_session.add(user)

    data = await state.get_data()
    question_index = data.get("question_index", choice(list(REACTIONS[field].keys())))

    reaction = REACTIONS[field][question_index].format(**{field: message.text})

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        await sleep(randint(2, 4))
        await message.answer(reaction)
        await sleep(randint(2, 4))

        random_index = randint(0, 9)
        if all(getattr(user, f) for f in ORDER):
            final_text = lexicon.results[random_index].format(
                space=user.space, budget=user.budget, geography=user.geography, style=user.style
            )
            final_reaction = lexicon.results_reaction[random_index]
            await message.answer(final_reaction)
            await sleep(randint(2, 4))
            await message.answer(final_text)
            await state.clear()
            await state.set_state(AIState.IN_AI_DIALOG)
        else:
            next_field, next_question = await ask_next_question(user, random_index)
            await state.set_state(getattr(Form, next_field))
            await state.update_data(question_index=random_index)
            await sleep(randint(2, 4))
            await message.answer(next_question)


@router.message(AIState.IN_AI_DIALOG, F.text)
async def ai_assistant_text_handler(
    message: Message, openai_client: AIClient, user: User, settings: Settings, db_session: AsyncSession
):
    thread_id = await check_ai_thread(user, openai_client, db_session)
    await message.forward(settings.bot.CHAT_LOG_ID)

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        response = await openai_client.get_response(thread_id, message.text)
        if response is None:
            await message.answer("Извините, я отвлекся, давайте начнём новый разговор.")
            return

        cleaned_response = refactor_string(response)
        msg_answer = await message.answer(cleaned_response, parse_mode=ParseMode.MARKDOWN_V2)
        await msg_answer.forward(settings.bot.CHAT_LOG_ID)


@router.message(AIState.IN_AI_DIALOG, F.voice)
async def ai_assistant_voice_handler(
    message: Message, openai_client: AIClient, user: User, settings: Settings, db_session: AsyncSession
):
    thread_id = await check_ai_thread(user, openai_client, db_session)
    await message.forward(settings.bot.CHAT_LOG_ID)
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        voice = message.voice
        file_info = await message.bot.get_file(voice.file_id)
        file_path = file_info.file_path

        file = await message.bot.download_file(file_path)
        audio_data = file.read()
        mp3_audio = await convert_to_mp3(audio_data)
        audio_stream = io.BytesIO(mp3_audio)
        audio_stream.name = "audio.mp3"
        try:
            transcription = await openai_client.client.audio.transcriptions.create(
                file=audio_stream, model="whisper-1", response_format="text"
            )
        except Exception as e:
            await message.reply("Error transcribing audio: " + str(e))
            return
        response = await openai_client.get_response(thread_id, transcription)
        if response is None:
            await message.answer("Извините, я отвлекся, давайте начнём новый разговор.")
            return
        cleaned_response = refactor_string(response)
        msg_answer = await message.answer(cleaned_response, parse_mode=ParseMode.MARKDOWN_V2)
        await msg_answer.forward(settings.bot.CHAT_LOG_ID)
