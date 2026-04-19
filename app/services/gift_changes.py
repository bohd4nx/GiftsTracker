from typing import Any

from pyrogram import Client

from .gift_crafts import notify_craft_models_changed
from .gift_upgrades import notify_upgrade_available, notify_upgrade_changed


def preserve_message_ids(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> None:
    for key in ["msg_id", "sticker_msg_id", "upgrade_msg_id", "emoji_id"]:
        if key in old_gift:
            new_gift[key] = old_gift[key]


def detect_upgrade_availability(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> bool:
    old_upgrade = old_gift.get("upgrade_price")
    new_upgrade = new_gift.get("upgrade_price")
    return old_upgrade is None and new_upgrade is not None and new_upgrade > 0


def detect_upgrade_price_change(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> bool:
    old_upgrade = old_gift.get("upgrade_price")
    new_upgrade = new_gift.get("upgrade_price")
    return (
        old_upgrade is not None
        and new_upgrade is not None
        and old_upgrade != new_upgrade
        and bool(old_gift.get("upgrade_msg_id"))
    )


def detect_craft_models_change(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> int | None:
    old_val = (old_gift.get("raw") or {}).get("upgrade_variants")
    new_val = (new_gift.get("raw") or {}).get("upgrade_variants")
    if old_val is not None and new_val is not None and new_val > old_val:
        return int(new_val) - int(old_val)
    return None


async def check_gift_changes(app: Client, _: Any, old_gift: dict[str, Any], new_gift: dict[str, Any]) -> bool:
    if detect_upgrade_availability(old_gift, new_gift):
        await notify_upgrade_available(app, new_gift)
        return True

    if detect_upgrade_price_change(old_gift, new_gift):
        await notify_upgrade_changed(app, new_gift, old_gift)
        return True

    if detect_craft_models_change(old_gift, new_gift):
        await notify_craft_models_changed(app, new_gift)
        return True

    return False
