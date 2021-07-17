import dataclasses
import enum
from typing import List, Optional, Tuple

from game.ecs.component import Component
from game.utils import Vector2


@dataclasses.dataclass
class Transform(Component):
    """Component that stores position information"""

    position: Vector2 = Vector2.ZERO


@dataclasses.dataclass
class Movement(Component):
    """Component that stores movement information"""

    direction: Vector2 = Vector2.ZERO
    h_scalar: int = 1
    v_scalar: int = 1
    last_position: Optional[Vector2] = None  # Used to cover up the last position


@dataclasses.dataclass
class PlayerInput(Component):
    """Component that maps player inputs"""

    up_keys: Tuple[str, ...] = (u'w', u'W')
    down_keys: Tuple[str, ...] = (u's', u'S')
    left_keys: Tuple[str, ...] = (u'a', u'A')
    right_keys: Tuple[str, ...] = (u'd', u'D')


@dataclasses.dataclass
class Renderable(Component):
    """Component that stores rendering data"""

    w: int = 1
    h: int = 1
    character: str = u'*'


@dataclasses.dataclass
class Text(Component):
    """Component that stores text for rendering"""

    class VerticalAlign(enum.IntEnum):
        TOP = 0
        CENTER = 1
        BOTTOM = 2

    class HorizontalAlign(enum.IntEnum):
        LEFT = 0
        CENTER = 1
        RIGHT = 2

    text_string: str = str()
    fg_color: str = 'green'
    bg_color: str = 'on_black'
    v_align: VerticalAlign = VerticalAlign.BOTTOM
    h_align: HorizontalAlign = HorizontalAlign.CENTER


@dataclasses.dataclass
class Ascii(Component):
    """Component that stores ascii text for rendering"""

    art: Optional[List[str]] = None
    fg_color: str = 'green'
    bg_color: str = 'on_black'


@dataclasses.dataclass
class TimeToLive(Component):
    """Component that tracks expirable entities"""

    start_time: Optional[float] = None
    current_time: Optional[float] = None
    expires_after: float = 5

    @property
    def expired(self) -> bool:
        """Return whether or not the component is expired"""
        return self.current_time - self.start_time >= self.expires_after


@dataclasses.dataclass
class FollowAI(Component):
    """Component that tracks another transform"""

    follow_transform: Optional[Transform] = None
    ticks_since_move: int = 0
