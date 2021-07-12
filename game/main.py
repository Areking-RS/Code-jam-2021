import dataclasses
import time
from functools import partial
from threading import Thread

from blessed import Terminal

from game.ecs.world import World, Component

echo = partial(print, end='', flush=True)


@dataclasses.dataclass
class Position(Component):
    x: int = 0
    y: int = 0


@dataclasses.dataclass
class Renderable(Component):
    w: int = 1
    h: int = 1
    character: str = u'*'


def movement_processor(term: Terminal):
    def _movement(dt, world):
        position_components = world.get_components(Position)
        for position in position_components:
            position.x += 1
            position.y += 1
    return _movement


def render_processor(term: Terminal):
    color_bg = term.on_blue
    echo(term.move_yx(1, 1))
    echo(color_bg(term.clear))
    color_worm = term.yellow_reverse

    def _renderer(dt, world: World):
        renderable_components = world.get_components(Renderable)
        for component in renderable_components:
            position = world.get_component(component.entity, Position)
            echo(term.move_yx(position.y, position.x))
            echo(color_worm(component.character))

    return _renderer


def main():
    term = Terminal()

    speed = 0.1
    modifier = 0.93
    inp = None

    world = World()
    world.create_entity(Position(x=5), Renderable(w=3, h=3, character=u'^'))
    world.create_entity(Position(y=5), Renderable(w=2, h=4, character=u'%'))
    world.register_processor(movement_processor(term))
    world.register_processor(render_processor(term))

    # Thread(target=game_loop).start()
    with term.hidden_cursor(), term.cbreak(), term.location():
        while inp not in (u'q', u'Q'):
            world.tick(0.0)
            inp = term.inkey(timeout=speed)


if __name__ == '__main__':
    main()
