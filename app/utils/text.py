from datetime import timedelta


def format_number(number: int) -> str:
    if number >= 1000:
        return "{:,}".format(number).replace(",", ".")
    return str(number)


def format_uptime(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if days or hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return ", ".join(parts)
