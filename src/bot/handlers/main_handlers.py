import asyncio
import random

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from src.bot.internal.callbacks import SpaceCallbackFactory
from src.bot.internal.dicts import texts
from src.bot.internal.enums import SpaceType
from src.bot.internal.keyboards import choose_space_kb
from src.bot.internal.states import States
from src.database.models import User

router = Router()


@router.message(F.photo)
async def handle_photo_info(message: Message, settings: Settings):
    if message.from_user.id not in settings.bot.ADMINS:
        return
    file_name = (message.photo[-1].file_id,)
    await message.answer(f"<b>File ID:</b> {file_name[0]}")


@router.message(CommandStart())
async def command_handler(
    message: Message,
    user: User,
    is_new_user: bool,
    db_session: AsyncSession,
) -> None:
    if is_new_user:
        await message.answer_photo(
            photo="AgACAgIAAxkBAAMFZ8CrNFHBNUVfWMUKrb5RcghTCeUAAoflMRvEfwhKuK1CG98mMu8BAAMCAAN5AAM2BA",
            caption=texts["welcome"],
        )
    else:
        if user.space_type is None:
            await message.answer(
                text=texts["space"],
                reply_markup=choose_space_kb(),
            )
        else:
            await message.answer('...')
        # await message.answer(texts['begin'])


@router.callback_query(SpaceCallbackFactory.filter())
async def players_multiselect_handler(
    callback: CallbackQuery,
    callback_data: SpaceCallbackFactory,
    user: User,
    state: FSMContext,
    db_session: AsyncSession,
) -> None:
    await callback.answer()
    match callback_data.choice:
        case SpaceType.INDOOR:
            user.space_type = SpaceType.INDOOR
            text = texts["indoor_area"]
        case SpaceType.OUTDOOR:
            user.space_type = SpaceType.OUTDOOR
            text = texts["outdoor_area"]
        case _:
            assert False, "Unexpected space type"
    db_session.add(user)
    await callback.message.answer(text=text)
    await state.set_state(States.INPUT_AREA)


@router.message(StateFilter(States))
async def input_entity(
    message: Message, user: User, state: FSMContext, db_session: AsyncSession
) -> None:
    current_state = await state.get_state()
    user_input = str(message.text)
    match current_state:
        case States.INPUT_AREA:
            user.area = user_input
            if not user.budget:
                text_budget = (
                    texts["indoor_budget"]
                    if user.space_type == SpaceType.INDOOR
                    else texts["outdoor_budget"]
                )
                await message.answer(text=text_budget)
                await state.set_state(States.INPUT_BUDGET)
        case States.INPUT_BUDGET:
            user.budget = str(user_input)
            budget_reply = (
                texts["indoor_budget_reply"]
                if user.space_type == SpaceType.INDOOR
                else texts["outdoor_budget_reply"]
            )
            await message.answer(text=budget_reply)
            if not user.geography:
                text_geo = (
                    texts["geo_indoor"]
                    if user.space_type == SpaceType.INDOOR
                    else texts["geo_outdoor"]
                )
                await asyncio.sleep(4)
                await message.answer(text=text_geo)
                await state.set_state(States.INPUT_GEOGRAPHY)
        case States.INPUT_GEOGRAPHY:
            user.geography = user_input
            text = texts["geo_reply"].format(user_input.capitalize())
            await message.answer(text=text)
            await asyncio.sleep(4)
            if not user.indoor_room and user.space_type == SpaceType.INDOOR:
                room_text = random.choice(
                    [texts["geo_indoor_room_1"], texts["geo_indoor_room_2"]]
                )
                await message.answer(text=room_text)
                next_state = States.INPUT_ROOM
            if not user.style and user.space_type == SpaceType.OUTDOOR:
                await message.answer(text=texts["outdoor_style"])
                next_state = States.INPUT_STYLE
            await state.set_state(next_state)
        case States.INPUT_ROOM:
            user.indoor_room = user_input
            if not user.style:
                await message.answer(text=texts["indoor_style"])
                await state.set_state(States.INPUT_STYLE)
        case States.INPUT_STYLE:
            user.style = user_input
            text_style = (
                texts["indoor_style_reply"].format(user_input.capitalize())
                if user.space_type == SpaceType.INDOOR
                else texts["outdoor_style_reply"].format(user_input.capitalize())
            )
            await message.answer(text=text_style)
            await asyncio.sleep(4)
            if not user.interests:
                text_interests = (
                    texts["indoor_interests"]
                    if user.space_type == SpaceType.INDOOR
                    else texts["outdoor_interests"]
                )
                await message.answer(text_interests)
                await state.set_state(States.INPUT_INTERESTS)
        case States.INPUT_INTERESTS:
            user.interests = user_input
            text_interests = (
                texts["confirmation_indoor"].format(user.area, user.style)
                if user.space_type == SpaceType.INDOOR
                else texts["confirmation_outdoor"]
            )
            await message.answer(text=text_interests)
            await asyncio.sleep(4)
            change_settings_text = (
                texts["change_settings_indoor"]
                if user.space_type == SpaceType.INDOOR
                else texts["change_settings_outdoor"]
            )
            await message.answer(text=change_settings_text)
    db_session.add(user)
