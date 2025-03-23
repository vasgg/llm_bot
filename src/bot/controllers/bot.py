from asyncio import sleep
import logging
from random import randint
import re

logger = logging.getLogger(__name__)


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(r"([%s])" % re.escape(escape_chars), r"\\\1", text)


def escape_stars(s):
    process = s.split("**")
    return "*".join([escape_markdown_v2(i) for i in process])


def extract_content(messages: list[dict[str, str]]) -> str:
    return " ".join(message["content"] for message in messages)


def starts_with_hash_space(s: str) -> bool:
    pattern = r"^#+\s"
    return bool(re.match(pattern, s))


def refactor_string(string: str) -> str:
    lines = string.splitlines()
    indices_to_wrap = []

    for i, line in enumerate(lines):
        if starts_with_hash_space(line):
            lines[i] = re.sub(r"^#+\s", "", line)
            indices_to_wrap.append(i)
        lines[i] = escape_stars(lines[i])

    for i in indices_to_wrap:
        lines[i] = f"*{lines[i]}*"

    return "\n".join(lines)


async def imitate_typing(delay_from=2, delay_to=4):
    await sleep(randint(delay_from, delay_to))
