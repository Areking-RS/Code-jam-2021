import dataclasses
import math
from functools import partial
from typing import ClassVar, Tuple, Union

Numeric = Union[int, float]


@dataclasses.dataclass
class Vector2(object):
    """Representation of 2D vectors and points."""

    x: Numeric = 0
    y: Numeric = 0

    ZERO: ClassVar['Vector2']
    UP: ClassVar['Vector2']
    DOWN: ClassVar['Vector2']
    LEFT: ClassVar['Vector2']
    RIGHT: ClassVar['Vector2']

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def to_tuple(self) -> Tuple[Numeric, Numeric]:
        """
        Get the tuple representation of this vector.

        :return: Tuple containing x and y coordinates
        """
        return self.x, self.y

    def add(self, other: 'Vector2') -> 'Vector2':
        """
        Add another vector to this vector.

        :param other: Vector to add
        :return: A new vector that is the addition of this vector and other
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __add__(self, other: 'Vector2'):
        return self.add(other)

    def sub(self, other: 'Vector2') -> 'Vector2':
        """
        Subtract another vector from this vector.

        :param other: Vector to subtract
        :return: A new vector that is the subtraction of other from self
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __sub__(self, other: 'Vector2'):
        return self.sub(other)

    def mag(self) -> Numeric:
        """Get the magnitude of this vector."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def scale(self, scalar: Numeric) -> 'Vector2':
        """
        Scale this vector by a scalar.

        :param scalar: A scalar to multiply this vector by
        :return: A scaled version of this vector
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __mul__(self, other: Numeric):
        return self.scale(other)

    def normalized(self) -> 'Vector2':
        """Get a normalized (unit) vector of this vector"""
        mag = self.mag()
        return Vector2() if mag == 0 else Vector2(self.x // mag, self.y // mag)


Vector2.ZERO = Vector2()
Vector2.UP = Vector2(0, -1)
Vector2.DOWN = Vector2(0, 1)
Vector2.LEFT = Vector2(-1, 0)
Vector2.RIGHT = Vector2(1, 0)
echo = partial(print, end='', flush=True)
