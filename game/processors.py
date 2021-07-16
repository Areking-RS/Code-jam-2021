import time
from typing import List

from blessed import Terminal

from game.components import Transform, Movement, Renderable, PlayerInput, Text, TimeToLive
from game.ecs.world import World
from game.utils import echo, Vector2


def movement_processor(term: Terminal, world: World, dt: float, inp: str):
    position_components = world.get_components(Transform)
    for transform in position_components:
        movement = world.get_component(transform.entity, Movement)
        if movement is not None:
            movement.last_position = transform.position
            transform.position = transform.position + movement.direction


def render_system(level_map: List[List[str]]):
    def _renderer(term: Terminal, world: World, dt: float, inp: str):
        color_bg = term.on_blue
        color_worm = term.yellow_reverse
        # Blank the screen
        echo(term.move_yx(1, 1))
        echo(color_bg(term.clear))

        # Draw the current map
        for row in level_map:
            print(term.orangered_on_blue(''.join(row)))

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


def input_processor(term: Terminal, world: World, dt: float, inp: str):
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


def text_renderer(term: Terminal, world: World, dt: float, inp: str):
    color_bg = term.on_blue
    # Blank the screen
    echo(term.move_yx(1, 1))
    echo(color_bg(term.clear))

    text_components = world.get_components(Text)
    for idx, text in enumerate(text_components):
        with term.location(0, term.height // 2 + idx):
            text_color = f'{text.fg_color}_{text.bg_color}'
            text_func = term.__getattr__(text_color)
            echo(term.center(text_func(text.text_string)))


def ttl_processor(term: Terminal, world: World, dt: float, inp: str):
    ttl_components = world.get_components(TimeToLive)
    for ttl in ttl_components:
        if ttl.start_time is None:
            ttl.start_time = time.monotonic()
        ttl.current_time = time.monotonic()