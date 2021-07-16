import dataclasses
from typing import Optional, Tuple

from game.ecs.component import Component
from game.utils import Vector2


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


@dataclasses.dataclass
class Text(Component):
    text_string: str = str()
    fg_color: str = 'green'
    bg_color: str = 'on_black'


@dataclasses.dataclass
class TimeToLive(Component):
    start_time: Optional[float] = None
    current_time: Optional[float] = None
    expires_after: float = 5

    @property
    def expired(self):
        return self.current_time - self.start_time >= self.expires_after