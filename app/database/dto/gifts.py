from dataclasses import dataclass
from typing import Any


@dataclass
class GiftsDTO:
    id: int
    price: int | None = None
    upgrade_price: int | None = None
    total_amount: int | None = None
    sticker_file_id: str | None = None
    sticker_msg_id: int | None = None
    msg_id: int | None = None
    upgrade_msg_id: int | None = None
    sticker_raw: dict | None = None
    raw: dict | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GiftsDTO":
        return cls(
            id=data["id"],
            price=data.get("price"),
            upgrade_price=data.get("upgrade_price"),
            total_amount=data.get("total_amount"),
            sticker_file_id=data.get("sticker_file_id"),
            sticker_msg_id=data.get("sticker_msg_id"),
            msg_id=data.get("msg_id"),
            upgrade_msg_id=data.get("upgrade_msg_id"),
            sticker_raw=data.get("sticker_raw"),
            raw=data.get("raw"),
        )
