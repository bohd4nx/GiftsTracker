import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parents[2] / "app.log"


def setup_logging() -> None:
    formatter = logging.Formatter(fmt="[%(asctime)s] - %(levelname)s: %(message)s", datefmt="%d.%m.%y %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler], force=True)

    logging.getLogger("aiogram.dispatcher").setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("pyrogram").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)
