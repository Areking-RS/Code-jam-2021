import asyncio
from typing import Callable, Coroutine


def entrypoint(func: Callable[[], Coroutine]):
    async def wrapper():
        try:
            exit_code = await func() or 0

        except KeyboardInterrupt:
            exit_code = 127

        exit(exit_code)

    asyncio.run(wrapper())
