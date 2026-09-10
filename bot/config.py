import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Config:
    bot_token: str = field(repr=False)


def load_config() -> Config:
    load_dotenv(PROJECT_ROOT / ".env")

    token = os.getenv("BOT_TOKEN", "").strip()

    if not token:
        raise RuntimeError()

    return Config(bot_token=token)