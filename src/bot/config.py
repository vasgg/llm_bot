from pydantic import SecretStr
from pydantic_settings import BaseSettings

from bot.internal.config_dicts import assign_config_dict


class BotConfig(BaseSettings):
    ADMINS: list[int]
    TOKEN: SecretStr
    CHAT_LOG_ID: int

    model_config = assign_config_dict(prefix="BOT_")


class GPTConfig(BaseSettings):
    OPENAI_API_KEY: SecretStr
    ASSISTANT_ID: SecretStr
    MODEL: str
    TEMPERATURE: float
    MAX_TOKENS: int
    PROMPT: str

    model_config = assign_config_dict(prefix="GPT_")


class DBConfig(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    NAME: str
    HOST: str
    PORT: int
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    model_config = assign_config_dict(prefix="DB_")

    @property
    def get_db_connection_string(self):
        return SecretStr(
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class Settings(BaseSettings):
    bot: BotConfig = BotConfig()
    gpt: GPTConfig = GPTConfig()
    db: DBConfig = DBConfig()

    model_config = assign_config_dict()
