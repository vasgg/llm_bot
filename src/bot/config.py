from pydantic import SecretStr
from pydantic_settings import BaseSettings

from bot.internal.enums import Stage
from bot.internal.helpers import assign_config_dict


class BotConfig(BaseSettings):
    ADMINS: list[int]
    TOKEN: SecretStr
    SENTRY_DSN: SecretStr | None = None
    CHAT_LOG_ID: int
    UTC_STARTING_MARK: int
    ACTIONS_THRESHOLD: int
    PICTURES_THRESHOLD: int
    PICTURES_WINDOW_DAYS: int
    USERS_THRESHOLD: int
    STAGE: Stage

    model_config = assign_config_dict(prefix="BOT_")


class ShopConfig(BaseSettings):
    ID: int
    PROVIDER_TOKEN: SecretStr

    model_config = assign_config_dict(prefix="SHOP_")


class GPTConfig(BaseSettings):
    OPENAI_API_KEY: SecretStr
    ASSISTANT_ID: SecretStr

    model_config = assign_config_dict(prefix="GPT_")


class RedisConfig(BaseSettings):
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: SecretStr

    model_config = assign_config_dict(prefix="REDIS_")


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
    shop: ShopConfig = ShopConfig()
    gpt: GPTConfig = GPTConfig()
    redis: RedisConfig = RedisConfig()
    db: DBConfig = DBConfig()

    model_config = assign_config_dict()


settings = Settings()
