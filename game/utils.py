import dataclasses
import math
from typing import ClassVar, Tuple


@dataclasses.dataclass
class Vector2(object):
    x: int = 0
    y: int = 0

    ZERO: ClassVar['Vector2']
    UP: ClassVar['Vector2']
    DOWN: ClassVar['Vector2']
    LEFT: ClassVar['Vector2']
    RIGHT: ClassVar['Vector2']

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    def add(self, other) -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __add__(self, other):
        return self.add(other)

    def sub(self, other) -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __sub__(self, other):
        return self.sub(other)

    def mag(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def scale(self, scalar) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)

    def __mul__(self, other):
        return self.scale(other)

    def normalized(self) -> 'Vector2':
        mag = self.mag()
        return Vector2() if mag == 0 else Vector2(self.x // mag, self.y // mag)


Vector2.ZERO = Vector2()
Vector2.UP = Vector2(0, -1)
Vector2.DOWN = Vector2(0, 1)
Vector2.LEFT = Vector2(-1, 0)
Vector2.RIGHT = Vector2(1, 0)
