import asyncio
from typing import Callable, Coroutine


def entrypoint(func: Callable[[], Coroutine]) -> None:
    """
    Run an async entrypoint, such as async `main()`.

    :param func: Async callable, typically `async def main()`
    :return: None
    """
    async def _wrapper() -> None:
        try:
            exit_code = await func() or 0

        except KeyboardInterrupt:
            exit_code = 127

        exit(exit_code)

    asyncio.run(_wrapper())
