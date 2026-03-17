from datetime import timedelta


def format_number(number: int) -> str:
    if number >= 1000:
        return "{:,}".format(number).replace(",", ".")
    return str(number)


def format_uptime(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())

    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)

    return " ".join(
        part
        for value, suffix in (
            (days, "d"),
            (hours, "h"),
            (minutes, "m"),
        )
        if value or suffix == "m"
        for part in [f"{value}{suffix}"]
    )
