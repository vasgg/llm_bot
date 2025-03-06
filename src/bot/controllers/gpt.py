import logging


from openai import AsyncOpenAI

from bot.config import Settings

logger = logging.getLogger(__name__)

#
# MODEL_PRICING = {
#     "gpt-4o": {
#         "prompt_tokens": 0.000005,  # $5 / 1M tokens
#         "completion_tokens": 0.000015,  # $15 / 1M tokens
#     },
#     "gpt-4o-mini": {
#         "prompt_tokens": 0.00000015,  # $0.15 / 1M tokens
#         "completion_tokens": 0.0000006,  # $0.6 / 1M tokens
#     },
#     "gpt-3.5-turbo-0125": {
#         "prompt_tokens": 0.0000005,  # $0.5 / 1M tokens
#         "completion_tokens": 0.0000015,  # $1.5 / 1M tokens
#     },
# }
#
#
# def calculate_api_cost(model: str, prompt_tokens: int, completion_tokens: int) -> Decimal:
#     if model not in MODEL_PRICING:
#         logger.warning(f"Unknown model: {model}. Using default pricing.")
#         model = "gpt-3.5-turbo-0125"
#
#     pricing = MODEL_PRICING[model]
#     prompt_cost = prompt_tokens * pricing["prompt_tokens"]
#     completion_cost = completion_tokens * pricing["completion_tokens"]
#     return prompt_cost + completion_cost
#
#
# def count_tokens(messages: List[Dict[str, str]], model: str) -> int:
#     try:
#         encoding = tiktoken.encoding_for_model(model)
#         num_tokens = 0
#         for message in messages:
#             num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
#             for key, value in message.items():
#                 num_tokens += len(encoding.encode(value))
#                 if key == "name":  # If there's a name, the role is omitted
#                     num_tokens -= 1  # Role is always required and always 1 token
#         num_tokens += 2  # Every reply is primed with <im_start>assistant
#         return num_tokens
#     except Exception as e:
#         logger.exception(f"Error counting tokens: {str(e)}")
#         return 0
#
#
# def truncate_messages(messages: List[dict], max_tokens: int, model: str) -> List[dict]:
#     truncated_messages = []
#     current_tokens = 0
#
#     # Always keep the system message
#     system_message = next((msg for msg in messages if msg["role"] == "system"), None)
#     if system_message:
#         truncated_messages.append(system_message)
#         current_tokens = count_tokens([system_message], model)
#
#     # Process the rest of the messages
#     for message in reversed(messages[1:]):  # Skip the system message
#         message_tokens = count_tokens([message], model)
#         if current_tokens + message_tokens <= max_tokens:
#             truncated_messages.insert(1, message)  # Insert after system message
#             current_tokens += message_tokens
#         else:
#             break
#
#     # Ensure the last message is from the user
#     if truncated_messages[-1]["role"] != "user":
#         user_messages = [msg for msg in reversed(messages) if msg["role"] == "user"]
#         if user_messages:
#             last_user_message = user_messages[0]
#             last_user_tokens = count_tokens([last_user_message], model)
#             if current_tokens + last_user_tokens <= max_tokens:
#                 truncated_messages.append(last_user_message)
#             else:
#                 # Truncate the last user message if necessary
#                 content = last_user_message["content"]
#                 while current_tokens + last_user_tokens > max_tokens:
#                     content = content[: -(len(content) // 10)]  # Remove 10% of the content
#                     last_user_tokens = count_tokens([{"role": "user", "content": content}], model)
#                 truncated_messages.append({"role": "user", "content": content})
#
#     return truncated_messages
#
#
# async def process_user_message(
#     openai_client: AsyncOpenAI,
#     user_id: UUID,
#     chat_id: int,
#     asset_ids: List[UUID],
#     db_session: AsyncSession,
# ) -> str:
#     try:
#         # Fetch chat history for context
#         chat_history = await get_last_messages(db_session, chat_id, limit=settings.MAX_PROMPT_MESSAGES)
#
#         # Fetch messages for semantic analysis
#         semantic_history_messages = await get_last_messages(db_session, chat_id, limit=settings.MAX_SEMANTIC_MESSAGES)
#
#         # Format semantic_chat_history
#         semantic_chat_history = "\n".join(
#             [f"{'Client' if msg['role'] == 'user' else 'Agent'}: {msg['content']}" for msg in semantic_history_messages]
#         )
#
#         # Get semantic prompt and prepare messages for semantic analysis
#         semantic_prompt = get_prompt(10)
#         semantic_messages = [
#             {"role": "system", "content": semantic_prompt["system_prompt"]},
#             {"role": "user", "content": semantic_chat_history},
#         ]
#
#         logger.info(f"Semantic message to GPT: {semantic_messages}")
#
#         try:
#             # Perform semantic analysis to determine the appropriate model
#             semantic_response = await openai_client.chat.completions.create(
#                 model=semantic_prompt["model"], messages=semantic_messages, max_tokens=10
#             )
#
#             semantic_result = semantic_response.choices[0].message.content.strip()
#             model_index = int(semantic_result) if semantic_result.isdigit() else settings.DEFAULT_PROMPT_INDEX
#
#             logger.info(f"Semantic Response: {semantic_result}")
#
#             # Calculate and store the cost for semantic analysis
#             semantic_usage = semantic_response.usage
#             semantic_cost = calculate_api_cost(
#                 semantic_prompt["model"], semantic_usage.prompt_tokens, semantic_usage.completion_tokens
#             )
#             await insert_openai_cost(
#                 user_id,
#                 semantic_usage.completion_tokens,
#                 semantic_usage.prompt_tokens,
#                 semantic_usage.total_tokens,
#                 semantic_prompt["model"],
#                 semantic_cost,
#                 db_session,
#             )
#
#         except Exception as e:
#             logger.exception(f"Error in semantic analysis: {str(e)}")
#             model_index = settings.DEFAULT_PROMPT_INDEX
#
#         # Get final prompt based on semantic analysis result
#         final_prompt = get_prompt(model_index)
#         filled_prompt = await fill_prompt_template(db_session, final_prompt["system_prompt"], user_id, asset_ids)
#
#         logger.info(f"Filled Prompt: {filled_prompt}")
#
#         # Prepare final messages for OpenAI API request
#         final_messages = [{"role": "system", "content": filled_prompt}, *chat_history]
#
#         # Determine the model and its token limit
#         model = final_prompt["model"]
#         max_tokens = 16385 if model == "gpt-3.5-turbo-0125" else 8192 if model == "gpt-4" else 4096
#
#         # Count tokens in final_messages
#         total_tokens = count_tokens(final_messages, model)
#         logger.info(f"Total tokens in final_messages: {total_tokens}")
#
#         # Truncate messages if they exceed the token limit
#         if total_tokens > max_tokens:
#             logger.warning(f"Messages exceed token limit. Truncating to fit within {max_tokens} tokens.")
#             final_messages = truncate_messages(final_messages, max_tokens, model)
#             total_tokens = count_tokens(final_messages, model)
#             logger.info(f"Total tokens after truncation: {total_tokens}")
#
#         try:
#             # Generate response using OpenAI API
#             final_response = await openai_client.chat.completions.create(
#                 model=model, messages=final_messages, max_tokens=4000
#             )
#
#             logger.info(f"Final Response: {final_response}")
#             logger.info(f"OpenAI reported token usage: {final_response.usage}")
#
#             # Calculate and store the cost for final response
#             final_usage = final_response.usage
#             final_cost = calculate_api_cost(model, final_usage.prompt_tokens, final_usage.completion_tokens)
#             await insert_openai_cost(
#                 user_id,
#                 final_usage.completion_tokens,
#                 final_usage.prompt_tokens,
#                 final_usage.total_tokens,
#                 model,
#                 final_cost,
#                 db_session,
#             )
#             return final_response.choices[0].message.content
#
#         except Exception as e:
#             logger.exception(f"Error in final OpenAI request: {str(e)}")
#             return "I apologize, but I encountered an error while processing your request. Please try again later."
#
#     except Exception as e:
#         logger.exception(f"Unexpected error in process_user_message: {str(e)}")
#         return "I'm sorry. Please try again later."
#
#
# async def process_messages_to_gpt(
#     message: types.Message,
#     state: FSMContext,
#     user_id: UUID,
#     openai_client: AsyncOpenAI,
#     transcribed_text: str = None,
# ):
#     await asyncio.sleep(3)
#
#     await show_typing(message.bot, message.chat.id)
#
#     is_valid, sanitized_message = await check_messages(str(combined_message))
#
#     if not is_valid:
#         sticker_file_id = 'CAACAgIAAxkBAAEMa71mhRbwAAHX1pBa9mitUzTqktsuZxIAAvoAA1advQpH3vqXcXRxATUE'
#         await message.bot.send_sticker(message.chat.id, sticker_file_id)
#     else:
#         try:
#             await insert_user_message(
#                 user_id,
#                 message.from_user.id,
#                 message.bot.id,
#                 message.chat.id,
#                 sanitized_message,
#                 Role.USER,
#                 db_session,
#             )
#
#             asset_ids = await determine_relevant_assets(message.from_user.id, db_session)
#
#             bot_response = await process_user_message(
#                 openai_client,
#                 user_id,
#                 message.chat.id,
#                 asset_ids,
#                 db_session,
#             )
#
#             bot_response_escaped = refactor_string(bot_response)
#             await message.reply(bot_response_escaped, parse_mode=ParseMode.MARKDOWN_V2)
#
#             await insert_bot_message(
#                 user_id,
#                 message.from_user.id,
#                 message.bot.id,
#                 message.chat.id,
#                 bot_response,
#                 Role.ASSISTANT,
#                 db_session,
#             )
#         except Exception as e:
#             logger.exception(f"Error in message processing: {str(e)}")
#             await message.reply("An error occurred while processing your request. Please try again later.")
#     await state.clear()
#
#
# async def process_user_history(extracted_content: str, openai_client: AsyncOpenAI) -> str:
#     prompt_file = 'src/gpt/prompts/promptdata/dialogsummary.md'
#     with open(prompt_file, encoding='utf-8') as file:
#         content = file.read()
#     completion = await openai_client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": content,
#             },
#             {"role": "user", "content": extracted_content},
#         ],
#     )
#     return completion.choices[0].message.content


async def generate_reply(prompt_text: str, openai_client: AsyncOpenAI, settings: Settings) -> str:
    response = await openai_client.chat.completions.create(
        model=settings.gpt.MODEL,
        messages=[{"role": "user", "content": prompt_text}],
        temperature=settings.gpt.TEMPERATURE,
        max_tokens=settings.gpt.MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()
