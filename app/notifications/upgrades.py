from app.core.constants import EMOJIS, FOOTER
from app.utils import format_number

e = EMOJIS


def create_upgrade_message_text(gift_data: dict, username: str | None = None) -> str:
    gift_id = gift_data.get("id")

    lines = [
        f"{e['title_upgrade']} <b>Gift upgrade available</b>\n",
        f"{e['gift_id']} <b>ID:</b> <code>{gift_id}</code>",
    ]

    if username:
        lines.append(f"{e['released_by']} <b>Released by:</b> @{username}")

    upgrade_price = format_number(gift_data.get("upgrade_price"))
    lines.append(
        f"{e['upgrade_price']} <b>Upgrade Price:</b> "
        f"<code>{upgrade_price}</code> {e['stars']}"
    )

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)
