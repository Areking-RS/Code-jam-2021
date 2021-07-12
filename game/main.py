import asyncio
import dataclasses
from threading import Thread

from game.ecs.world import World, Component
from utils import entrypoint


@dataclasses.dataclass
class Position(Component):
    x: int = 0
    y: int = 0


async def movement_processor(world):
    position_components = world.get_components(Position)
    for position in position_components:
        position.x += 1
        position.y += 1

        print(f"Moved Entity-{position.entity} to ({position.x}, {position.y})")

    await asyncio.sleep(1)


@entrypoint
async def main():
    world = World()
    world.create_entity(Position())
    world.create_entity(Position())
    world.register_processor(movement_processor)

    def _server():
        async def _wrapper():
            while True:
                await world.tick()

        asyncio.run(_wrapper())

    Thread(target=_server).start()
