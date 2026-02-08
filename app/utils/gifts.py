def preserve_message_ids(old_gift: dict, new_gift: dict) -> None:
    for key in ["msg_id", "sticker_msg_id", "upgrade_msg_id"]:
        if key in old_gift:
            new_gift[key] = old_gift[key]


def detect_upgrade_availability(old_gift: dict, new_gift: dict) -> bool:
    old_upgrade = old_gift.get("upgrade_price")
    new_upgrade = new_gift.get("upgrade_price")
    return old_upgrade is None and new_upgrade is not None and new_upgrade > 0


def detect_upgrade_price_change(old_gift: dict, new_gift: dict) -> bool:
    old_upgrade = old_gift.get("upgrade_price")
    new_upgrade = new_gift.get("upgrade_price")
    return (
        old_upgrade is not None
        and new_upgrade is not None
        and old_upgrade != new_upgrade
        and old_gift.get("upgrade_msg_id")
    )
