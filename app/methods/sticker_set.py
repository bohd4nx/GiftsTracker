import asyncio
import logging

from pyrogram import Client, raw

logger = logging.getLogger(__name__)


def make_sticker_item(sticker) -> raw.types.InputStickerSetItem:
    """Creates an InputStickerSetItem from a dict or a raw Document object."""
    if isinstance(sticker, dict):
        doc_id, access_hash, file_reference = (
            sticker["id"],
            sticker["access_hash"],
            sticker["file_reference"],
        )
    else:
        doc_id, access_hash, file_reference = (
            sticker.id,
            sticker.access_hash,
            sticker.file_reference,
        )
    return raw.types.InputStickerSetItem(
        document=raw.types.InputDocument(
            id=doc_id,
            access_hash=access_hash,
            file_reference=file_reference,
        ),
        emoji="🎁",
    )


async def create_sticker_set(
    app: Client,
    user_peer,
    title: str,
    short_name: str,
    first_item: raw.types.InputStickerSetItem,
) -> tuple[raw.types.InputStickerSetID, int]:
    """Creates a custom emoji pack with a single initial sticker.

    Returns (InputStickerSetID, first_emoji_id).
    """
    result: raw.types.messages.StickerSet = await app.invoke(  # type: ignore[assignment]
        raw.functions.stickers.CreateStickerSet(  # type: ignore[arg-type]
            user_id=user_peer,
            title=title,
            short_name=short_name,
            stickers=[first_item],
            emojis=True,
        )
    )
    await asyncio.sleep(2)
    ref = raw.types.InputStickerSetID(
        id=result.set.id,
        access_hash=result.set.access_hash,
    )
    return ref, result.documents[0].id


async def add_sticker_to_set(
    app: Client,
    stickerset_ref,
    item: raw.types.InputStickerSetItem,
) -> raw.types.messages.StickerSet:
    return await app.invoke(  # type: ignore[return-value]
        raw.functions.stickers.AddStickerToSet(  # type: ignore[arg-type]
            stickerset=stickerset_ref,
            sticker=item,
        )
    )


async def get_sticker_set(app: Client, stickerset_ref) -> raw.types.messages.StickerSet:
    return await app.invoke(  # type: ignore[return-value]
        raw.functions.messages.GetStickerSet(  # type: ignore[arg-type]
            stickerset=stickerset_ref,
            hash=0,
        )
    )
