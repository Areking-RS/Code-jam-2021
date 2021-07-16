import dataclasses
import time
from functools import partial
from threading import Thread
from typing import List, Optional, Tuple

from blessed import Terminal

from game.ecs.world import Component, World
from game.mapgeneration import mapgenerator
from game.utils import Vector2

echo = partial(print, end='', flush=True)
current_map = mapgenerator(
    map_width=50,
    map_height=50,
    room_frequency=3,
    room_size=30,
    path_width=5
    )
spawn=current_map[1]
current_map=current_map[0]




@dataclasses.dataclass
class Transform(Component):
    position: Vector2 = Vector2.ZERO


@dataclasses.dataclass
class Movement(Component):
    direction: Vector2 = Vector2.ZERO
    h_scalar: int = 1
    v_scalar: int = 1
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
                next_pos=transform.position+movement.direction

                if (current_map[next_pos.y])[next_pos.x]=='#':
                    movement.last_position = transform.position
                    #print(transform.position)
                else:
                    transform.position = transform.position + movement.direction
                    #print(transform.position)

    return _movement


def render_system(term: Terminal, level_map: List[List[str]]):
    color_bg = term.on_white
    color_worm = term.green_reverse

    def _renderer(dt, world: World, inp: str):
        # Blank the screen
        echo(term.move_yx(1, 1))
        echo(color_bg(term.clear))

        # Draw the current map
        for row in level_map:
            print(term.black_on_white(''.join(row)))

        # Draw the Renderable components
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
        renderable = world.get_component(component.entity, Renderable)

        if movement is not None:
            # TODO: Shouldn't apply scalars here, instead should correctly apply them in the movement processor
            if inp in component.up_keys:
                movement.direction = Vector2.UP * movement.v_scalar
                renderable.character = u'^'
            elif inp in component.down_keys:
                movement.direction = Vector2.DOWN * movement.v_scalar
                renderable.character = u'v'
            elif inp in component.left_keys:
                movement.direction = Vector2.LEFT * movement.h_scalar
                renderable.character = u'<'
            elif inp in component.right_keys:
                movement.direction = Vector2.RIGHT * movement.h_scalar
                renderable.character = u'>'
            else:
                movement.direction=Vector2.ZERO

def main():
    term = Terminal()

    speed = 1/10
    inp = None

    world = World()
    world.create_entity(
        Transform(position=Vector2(x=spawn )),
        Movement(direction=Vector2.DOWN),
        PlayerInput(),
        Renderable(w=1, h=1, character=u'^')
    )



    world.register_processor(input_processor)
    world.register_processor(movement_processor(term))


    world.register_processor(render_system(term, current_map))

    # Thread(target=game_loop).start()
    with term.hidden_cursor(), term.cbreak(), term.location():
        while inp not in (u'q', u'Q'):
            world.tick(0.0, inp)
            inp = term.inkey(timeout=speed)


if __name__ == '__main__':
    main()
