from app.utils import format_number

EMOJIS = {
    'party': '<emoji id="5411480216809792207">🎁</emoji>',
    'released': '<emoji id="5409129417999936997">✅</emoji>',
    'price': '<emoji id="5409181322679706928">ℹ️</emoji>',
    'star': '<emoji id="5472092560522511055">⭐️</emoji>',
    'rounds': '<emoji id="5411180428092533606">🔨</emoji>',
    'premium': '<emoji id="5409044699770026104">🔒</emoji>',
    'upgrade': '<emoji id="5409128576186347318">⬆️</emoji>',
    'settings': '<emoji id="5409102321051266958">⚙️</emoji>',
    'search': '<emoji id="5424894868554018540">🔎</emoji>',
}

FOOTER = (
    '<emoji id="5418343793592135531">🏪</emoji> '
    '<a href="https://t.me/portals/market?startapp=mxavdf">Portals</a>'
    ' • '
    '<emoji id="5418239967052724167">🏪</emoji> '
    '<a href="https://t.me/tonnel_network_bot/gifts?startapp=ref_5616264938">Tonnel</a>'
)


def create_message_text(
        gift_data: dict,
        username: str | None = None,
        is_upgrade: bool = False
) -> str:
    raw_data = gift_data.get("raw", {})
    gift_id = gift_data.get("id")

    title = "Gift upgrade available" if is_upgrade else "New gift available"
    title_emoji = EMOJIS["search"] if is_upgrade else EMOJIS["party"]

    lines = [f"{title_emoji} <b>{title}</b>\n"]
    lines.append(f"{EMOJIS['settings']} <b>ID:</b> <code>{gift_id}</code>")

    if username:
        lines.append(f"{EMOJIS['released']} <b>Released by:</b> @{username}")

    if is_upgrade:
        upgrade_price = format_number(gift_data.get("upgrade_price"))
        lines.append(
            f"{EMOJIS['upgrade']} <b>Upgrade Price:</b> "
            f"<code>{upgrade_price}</code> {EMOJIS['star']}"
        )
    else:
        price = format_number(gift_data["price"])
        price_line = (
            f"{EMOJIS['price']} <b>Price:</b> "
            f"<code>{price}</code>{EMOJIS['star']}"
        )

        if total_amount := gift_data.get("total_amount"):
            price_line += f" | <b>Supply:</b> <code>{format_number(total_amount)}</code>"

        lines.append(price_line)

        if raw_data.get("auction") and (gifts_per_round := raw_data.get("gifts_per_round")):
            rounds = (gift_data.get("total_amount") or 0) // gifts_per_round
            lines.append(
                f"{EMOJIS['rounds']} <b>{rounds}</b> rounds • "
                f"<b>{gifts_per_round}</b> per round"
            )

        limits = []

        if raw_data.get("require_premium"):
            limits.append("<b>Premium Only</b>")

        if per_user := raw_data.get("per_user_total"):
            limits.append(f"<b>{per_user}</b> per user")

        if limits:
            lines.append(f"{EMOJIS['premium']} {' • '.join(limits)}")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)
