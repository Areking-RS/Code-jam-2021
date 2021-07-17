import time

from blessed import Terminal

from game.components import (
    Ascii, Movement, PlayerInput, Renderable, Text, TimeToLive, Transform
)
from game.ecs import ProcessorFunc
from game.ecs.world import World
from game.mapgeneration import MapType
from game.utils import Vector2, echo


def movement_processor(current_map: MapType) -> ProcessorFunc:
    """Returns a processor that handles movement for the given map"""

    def movement(term: Terminal, world: World, dt: float, inp: str) -> None:
        position_components = world.get_components(Transform)
        for transform in position_components:
            movement = world.get_component(transform.entity, Movement)
            if movement is not None:
                movement.last_position = transform.position
                next_pos = transform.position + movement.direction

                if (current_map[next_pos.y])[next_pos.x] == '#':
                    movement.last_position = transform.position
                else:
                    transform.position = transform.position + movement.direction

    return movement


def render_system(level_map: MapType) -> ProcessorFunc:
    """Returns a processor that renders entities on the given map"""

    def _renderer(term: Terminal, world: World, dt: float, inp: str) -> None:
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


def input_processor(term: Terminal, world: World, dt: float, inp: str) -> None:
    """Processor that handles inputs for PlayerInput components"""
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
                movement.direction = Vector2.ZERO


def text_renderer(term: Terminal, world: World, dt: float, inp: str) -> None:
    """Renders text components"""
    # color_bg = term.on_blue
    # # Blank the screen
    # echo(term.move_yx(1, 1))
    # echo(color_bg(term.clear))

    text_components = world.get_components(Text)
    for idx, text in enumerate(text_components):
        text_color = f'{text.fg_color}_{text.bg_color}'
        text_func = term.__getattr__(text_color)

        if text.h_align == Text.HorizontalAlign.LEFT:
            h_align = term.ljust
        elif text.h_align == Text.HorizontalAlign.CENTER:
            h_align = term.center
        elif text.h_align == Text.HorizontalAlign.RIGHT:
            h_align = term.rjust
        else:
            h_align = term.ljust

        if text.v_align == Text.VerticalAlign.TOP:
            y_offset = 0
        elif text.v_align == Text.VerticalAlign.CENTER:
            y_offset = term.height // 2
        elif text.v_align == Text.VerticalAlign.BOTTOM:
            y_offset = term.height - 1
        else:
            y_offset = 0

        with term.location(0, y_offset):
            echo(h_align(text_func(text.text_string)))


def ascii_renderer(term: Terminal, world: World, dt: float, inp: str) -> None:
    """Renders text components"""
    # color_bg = term.on_blue
    # # Blank the screen
    # echo(term.move_yx(1, 1))
    # echo(color_bg(term.clear))

    ascii_components = world.get_components(Ascii)
    center_height = term.height // 2
    for ascii in ascii_components:
        half_art_len = len(ascii.art) // 2
        base_offset = center_height - half_art_len
        for idx, line in enumerate(ascii.art):
            with term.location(0, base_offset + idx):
                text_color = f'{ascii.fg_color}_{ascii.bg_color}'
                text_func = term.__getattr__(text_color)
                echo(term.center(text_func(line)))


def ttl_processor(term: Terminal, world: World, dt: float, inp: str) -> None:
    """Process lifetimes for TimeToLive components"""
    ttl_components = world.get_components(TimeToLive)
    for ttl in ttl_components:
        if ttl.start_time is None:
            ttl.start_time = time.monotonic()
        ttl.current_time = time.monotonic()
