from app.notifications.constants import EMOJIS, FOOTER
from app.utils import format_number


def create_gift_message_text(
        gift_data: dict,
        username: str | None = None
) -> str:
    raw_data = gift_data.get("raw", {})
    gift_id = gift_data.get("id")

    lines = [f"{EMOJIS['title_new_gift']} <b>New gift available</b>\n",
             f"{EMOJIS['gift_id']} <b>ID:</b> <code>{gift_id}</code>"]

    if username:
        lines.append(f"{EMOJIS['released_by']} <b>Released by:</b> @{username}")

    price = format_number(gift_data["price"])
    price_line = (
        f"{EMOJIS['price']} <b>Price:</b> "
        f"<code>{price}</code>{EMOJIS['stars']}"
    )

    if total_amount := gift_data.get("total_amount"):
        price_line += f" | <b>Supply:</b> <code>{format_number(total_amount)}</code>"

    lines.append(price_line)

    if raw_data.get("auction") and (gifts_per_round := raw_data.get("gifts_per_round")):
        rounds = (gift_data.get("total_amount") or 0) // gifts_per_round
        lines.append(
            f"{EMOJIS['auction_rounds']} <b>{rounds}</b> rounds • "
            f"<b>{gifts_per_round}</b> per round"
        )

    limits = []

    if raw_data.get("require_premium"):
        limits.append("<b>Premium Only</b>")

    if per_user := raw_data.get("per_user_total"):
        limits.append(f"<b>{per_user}</b> per user")

    if limits:
        lines.append(f"{EMOJIS['premium']} {' • '.join(limits)}")

    if raw_data.get("locked_until_date"):
        lines.append(f"{EMOJIS['restrictions']} <b>Time Locked</b>")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)
