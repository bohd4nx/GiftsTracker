from typing import Any

from app.core.constants import EMOJIS, FOOTER
from app.utils import gift_emoji

e = EMOJIS


def create_craft_message_text(gift_data: dict[str, Any], delta: int, username: str | None = None) -> str:
    gift_id = gift_data.get("id")

    lines = [
        f"{gift_emoji(gift_data)} <b>Gift craft available</b> • {delta} models\n",
        f"{e['gift_id']} <b>ID:</b> <code>{gift_id}</code>",
    ]

    if username:
        lines.append(f"{e['released_by']} <b>Released by:</b> @{username}")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)
