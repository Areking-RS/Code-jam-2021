import dataclasses
import time
from functools import partial
from threading import Thread
from typing import List, Tuple, Optional

from blessed import Terminal

from game.ecs.world import World, Component
from game.utils import Vector2

echo = partial(print, end='', flush=True)


@dataclasses.dataclass
class Transform(Component):
    position: Vector2 = Vector2.ZERO


@dataclasses.dataclass
class Movement(Component):
    direction: Vector2 = Vector2.ZERO
    last_position: Optional[Vector2] = None  # Used to cover up the last position


@dataclasses.dataclass
class PlayerInput(Component):
    up_keys: Tuple[str, ...] = (u'w', u'W')
    down_keys: Tuple[str, ...] = (u's', u'S')
    left_keys: Tuple[str, ...] = (u'a', u'A')
    right_keys: Tuple[str, ...] = (u'd', u'D')


@dataclasses.dataclass
class Renderable(Component):
    w: int = 1
    h: int = 1
    character: str = u'*'


def movement_processor(term: Terminal):
    def _movement(dt, world: World, inp: str):
        position_components = world.get_components(Transform)
        for transform in position_components:
            movement = world.get_component(transform.entity, Movement)
            if movement is not None:
                movement.last_position = transform.position
                transform.position = transform.position + movement.direction
    return _movement


def render_processor(term: Terminal):
    color_bg = term.on_blue
    echo(term.move_yx(1, 1))
    echo(color_bg(term.clear))
    color_worm = term.yellow_reverse

    def _renderer(dt, world: World, inp: str):
        renderable_components = world.get_components(Renderable)
        for component in renderable_components:
            transform = world.get_component(component.entity, Transform)
            movement = world.get_component(component.entity, Movement)

            # Clear the old position
            if movement is not None and movement.last_position is not None:
                echo(term.move_xy(*movement.last_position))
                for i in range(component.h):
                    echo(color_bg(u' ' * component.w))
                    echo(term.move_xy(*(movement.last_position + Vector2(0, -(i + 1)))))

            # Draw the new position
            echo(term.move_xy(*transform.position))
            for i in range(component.h):
                echo(color_worm(component.character * component.w))
                echo(term.move_xy(*(transform.position + Vector2(0, -(i + 1)))))

    return _renderer


def input_processor(dt, world: World, inp: str):
    player_inputs = world.get_components(PlayerInput)
    for component in player_inputs:
        movement = world.get_component(component.entity, Movement)
        if movement is not None:
            if inp in component.up_keys:
                movement.direction = Vector2.UP
            elif inp in component.down_keys:
                movement.direction = Vector2.DOWN
            elif inp in component.left_keys:
                movement.direction = Vector2.LEFT
            elif inp in component.right_keys:
                movement.direction = Vector2.RIGHT


def main():
    term = Terminal()

    speed = 1/15
    inp = None

    world = World()
    world.create_entity(
        Transform(),
        Movement(direction=Vector2.RIGHT),
        PlayerInput(),
        Renderable(w=3, h=3, character=u'^')
    )

    world.create_entity(
        Transform(position=Vector2(x=5)),
        Movement(direction=Vector2.RIGHT),
        PlayerInput(),
        Renderable(w=2, h=4, character=u'%')
    )

    world.register_processor(input_processor)
    world.register_processor(movement_processor(term))
    world.register_processor(render_processor(term))

    # Thread(target=game_loop).start()
    with term.hidden_cursor(), term.cbreak(), term.location():
        while inp not in (u'q', u'Q'):
            world.tick(0.0, inp)
            inp = term.inkey(timeout=speed)


if __name__ == '__main__':
    main()
