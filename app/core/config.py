import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"

        if not env_path.exists():
            logger.error("Configuration file not found! Please create '.env'")
            sys.exit(1)

        load_dotenv(env_path)

        self.API_ID: int = int(os.getenv("API_ID", "0"))
        self.API_HASH: str = os.getenv("API_HASH", "")
        self.PHONE_NUMBER: str = os.getenv("PHONE_NUMBER", "")
        self.PASSWORD: str | None = os.getenv("PASSWORD") or None

        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

        self.CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", "0"))
        self.STICKERS_CHANNEL_ID: int = int(os.getenv("STICKERS_CHANNEL_ID", "0"))
        self.STICKERS_CHANNEL_USERNAME: str = os.getenv("STICKERS_CHANNEL_USERNAME", "")

        self.INTERVAL: float = float(os.getenv("INTERVAL", "15.0"))


config = Config()
