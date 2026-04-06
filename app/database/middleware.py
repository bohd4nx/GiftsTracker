import functools
from collections.abc import Callable, Awaitable
from typing import Any


from .base import SessionLocal


def with_session(
    handler: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]:
    """Decorator that injects an AsyncSession as the last positional argument.

    Usage::

        @with_session
        async def handle_status(client, message, session: AsyncSession):
            total = await GiftsCRUD.count(session)
            ...
    """

    @functools.wraps(handler)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with SessionLocal() as session:
            return await handler(*args, session, **kwargs)

    return wrapper
