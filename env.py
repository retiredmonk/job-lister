from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DISCORD_ID: str
    DISCORD_TOKEN: str

    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str

    SLACK_URL: str

    POLL_INTERVAL: int

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()