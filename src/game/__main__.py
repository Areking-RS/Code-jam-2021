import asyncio
import time
from threading import Thread

from ecs.component import Component
from ecs.world import World
from utils import entrypoint

world = World()


class Position(Component):
    """Position component for entities."""

    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


class Collider(Component):
    """Collider component for entities."""


async def movement_processor() -> None:
    """
    Movement processor for entities.

    :return: None
    """
    for entity, (position, *_) in world.get_components(Position):
        position.x += 1 + position.id
        position.y += 1 + position.id

        print(f"[{int(time.time())}] Moved Entity-{position.id} to ({position.x}, {position.y})")

        if entity == 1:
            await asyncio.sleep(1.000)

        await asyncio.sleep(1.000)


async def map_processor() -> None:
    for entity, (position, _collider) in world.get_components(Position, Collider):
        pass


@entrypoint
async def main() -> None:
    """
    Main function, which serves as an entrypoint for this project.

    :return: None
    """
    world.create_entity(Position())
    world.create_entity(Position())

    world.register_processor(movement_processor)

    def _server() -> None:
        async def _wrapper() -> None:
            while True:
                await world.tick()

        asyncio.run(_wrapper())

    Thread(target=_server).start()
