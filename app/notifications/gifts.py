from app.core.constants import EMOJIS, FOOTER
from app.utils import format_number, gift_emoji

e = EMOJIS


def create_gift_message_text(gift_data: dict, username: str | None = None) -> str:
    raw_data = gift_data.get("raw", {})
    gift_id = gift_data.get("id")

    lines = [
        f"{gift_emoji(gift_data)} <b>New gift available</b>\n",
        f"{e['gift_id']} <b>ID:</b> <code>{gift_id}</code>",
    ]

    if username:
        lines.append(f"{e['released_by']} <b>Released by:</b> @{username}")

    price = format_number(gift_data["price"])
    price_line = f"{e['price']} <b>Price:</b> <code>{price}</code>{e['stars']}"

    if total_amount := gift_data.get("total_amount"):
        price_line += f" • <b>Supply:</b> <code>{format_number(total_amount)}</code>"

    lines.append(price_line)

    if raw_data.get("auction") and (gifts_per_round := raw_data.get("gifts_per_round")):
        rounds = (gift_data.get("total_amount") or 0) // gifts_per_round
        lines.append(
            f"{e['auction_rounds']} <b>{rounds}</b> rounds • "
            f"<b>{gifts_per_round}</b> per round"
        )

    limits = []

    if raw_data.get("require_premium"):
        limits.append("<b>Premium Only</b>")

    if per_user := raw_data.get("per_user_total"):
        limits.append(f"<b>{per_user}</b> per user")

    if limits:
        lines.append(f"{e['premium']} {' • '.join(limits)}")

    if raw_data.get("locked_until_date"):
        lines.append(f"{e['restrictions']} <b>Time Locked</b>")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)
