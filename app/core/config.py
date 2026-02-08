import logging
import sys
from configparser import ConfigParser
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        config_path = Path(__file__).resolve().parents[2] / "config.ini"

        if not config_path.exists():
            logger.error("Configuration file not found! Please create 'config.ini'")
            sys.exit(1)

        parser = ConfigParser()
        parser.read(config_path, encoding="utf-8")

        self.API_ID: int = parser.getint("Telegram", "API_ID")
        self.API_HASH: str = parser.get("Telegram", "API_HASH")
        self.PHONE_NUMBER: str = parser.get("Telegram", "PHONE_NUMBER")
        self.PASSWORD: str | None = parser.get("Telegram", "PASSWORD", fallback=None) or None

        self.BOT_TOKEN: str = parser.get("Telegram", "BOT_TOKEN")

        self.CHANNEL_ID: int = parser.getint("Channels", "CHANNEL_ID")
        self.STICKERS_CHANNEL_ID: int = parser.getint("Channels", "STICKERS_CHANNEL_ID")
        self.STICKERS_CHANNEL_USERNAME: str = parser.get("Channels", "STICKERS_CHANNEL_USERNAME")

        self.INTERVAL: float = parser.getfloat("Tracker", "INTERVAL", fallback=15.0)


config = Config()
