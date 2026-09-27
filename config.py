import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    api_base_url: str
    db_path: str


def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN не задан")

    return Config(
        bot_token=token,
        api_base_url=os.getenv("API_BASE_URL", "http://localhost:9090").rstrip("/"),
        db_path=os.getenv("DB_PATH", "./gradinator_bot.sqlite3"),
    )
