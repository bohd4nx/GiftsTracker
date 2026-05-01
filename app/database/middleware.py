import functools
from collections.abc import Awaitable, Callable
from typing import Any

from .base import SessionLocal


def with_session(
    handler: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """Decorator that opens an AsyncSession and injects it as the last positional arg."""

    @functools.wraps(handler)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with SessionLocal() as session:
            return await handler(*args, session, **kwargs)

    return wrapper
