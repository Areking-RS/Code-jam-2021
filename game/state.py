from typing import Optional

from blessed import Terminal

from game.components import (
    Movement, PlayerInput, Renderable, Text, TimeToLive, Transform
)
from game.ecs.world import World
from game.mapgeneration import mapgenerator
from game.processors import (
    input_processor, movement_processor, render_system, text_renderer,
    ttl_processor
)
from game.utils import Vector2


class Screen(object):
    def __init__(self, world: Optional[World] = None):
        if world is None:
            world = World()
        self.world = world

    def setup(self, term: Terminal):
        pass

    def tick(self, term: Terminal, dt: float, inp: str) -> Optional['Screen']:
        self.world.tick(term, dt, inp)
        return None


class Intro(Screen):
    def __init__(self):
        super(Intro, self).__init__()
        self.text_entity: Optional[int] = None
        self.ttl_component: Optional[TimeToLive] = None

    def setup(self, term: Terminal):
        text = Text(text_string='Dedicated Dugongs')
        self.ttl_component = TimeToLive(expires_after=1)
        self.text_entity = self.world.create_entity(text, self.ttl_component)
        self.world.register_processor(text_renderer)
        self.world.register_processor(ttl_processor)

    def tick(self, term: Terminal, dt: float, inp: str) -> Optional['Screen']:
        super(Intro, self).tick(term, dt, inp)
        if self.ttl_component.expired:
            return GameLevel()


class GameLevel(Screen):
    def __init__(self):
        super(GameLevel, self).__init__()

    def setup(self, term: Terminal):
        self.world.register_processor(input_processor)

        current_map = mapgenerator(
            map_width=50,
            map_height=50,
            room_frequency=10,
            room_size=30,
            path_width=5
        )
        spawn = current_map[1]
        current_map = current_map[0]

        self.world.create_entity(
            Transform(position=Vector2(x=spawn)),
            Movement(direction=Vector2.RIGHT),
            PlayerInput(),
            Renderable(w=1, h=1, character=u'^')
        )

        self.world.register_processor(movement_processor(current_map))
        self.world.register_processor(render_system(current_map))
