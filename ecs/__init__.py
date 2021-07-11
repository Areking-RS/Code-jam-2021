from ._component import Component
from ._world import World


async def main():
    import asyncio
    import time
    from threading import Thread

    class Position(Component):
        x: int = 0
        y: int = 0

        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

    world = World()

    async def movement_processor():
        for pos in world.get_components(Position):
            pos.x += 1 + pos.id
            pos.y += 1 + pos.id

            print(f"Moved Entity.{pos.id} to ({pos.x = }, {pos.y = })")

        await asyncio.sleep(1)

    world.register_processor(movement_processor)

    e0 = world.create_entity(Position(0, 0))
    _e1 = world.create_entity(Position(69, 420))

    world.delete_entity(e0)

    def server():
        async def _f():
            while True:
                await world.tick()

        asyncio.run(_f())

    Thread(target=server).start()

    time.sleep(1.000)

    world.create_entity(Position(0, 0))

    time.sleep(0.500)

    world.remove_processor(movement_processor)


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Exiting...")
