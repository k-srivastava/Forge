"""
Two-dimensional vectors in Forge.
"""
from __future__ import annotations

import dataclasses
import math
import random as rand


@dataclasses.dataclass(slots=True)
class Vector2D:
    """
    Forge's representation of a two-dimensional vector.
    """
    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vector2D) -> Vector2D:
        self.x += other.x
        self.y += other.y

        return self

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vector2D) -> Vector2D:
        self.x -= other.x
        self.y -= other.y

        return self

    def __mul__(self, scalar: int | float) -> Vector2D:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __imul__(self, scalar: int | float) -> Vector2D:
        self.x *= scalar
        self.y *= scalar

        return self

    def __truediv__(self, scalar: int | float) -> Vector2D:
        return Vector2D(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar: int | float) -> Vector2D:
        self.x /= scalar
        self.y /= scalar

        return self

    def __floordiv__(self, scalar: int | float) -> Vector2D:
        return Vector2D(self.x // scalar, self.y // scalar)

    def __ifloordiv__(self, scalar: int | float) -> Vector2D:
        self.x //= scalar
        self.y //= scalar

        return self

    def __eq__(self, other: Vector2D) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Vector2D) -> bool:
        return self.x != other.x or self.y != other.y

    def __abs__(self) -> Vector2D:
        return Vector2D(abs(self.x), abs(self.y))

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __bool__(self) -> bool:
        return self.x != 0 and self.y != 0

    def __copy__(self) -> Vector2D:
        return Vector2D(self.x, self.y)

    def __repr__(self) -> str:
        return f'Vector -> x: {self.x:.3f}, y: {self.y:.3f}'

    def __str__(self) -> str:
        return f'Forge Vector2D -> x: {self.x}, y: {self.y}, length: {self.length()}'

    def length(self) -> float:
        """
        Compute the length of the vector.

        :return: Length or magnitude of the vector.
        :rtype: float
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def length_squared(self) -> float:
        """
        Compute the square of the length of the vector. Faster due to lack of a square root operation.

        :return: Square of the length or magnitude of the vector.
        :rtype: float
        """
        return self.x ** 2 + self.y ** 2

    def normalize(self) -> None:
        """
        Normalize the vector, i.e., set its length to one while maintaining the same direction.

        :raises ZeroDivisionError: A vector of zero length cannot be normalized.
        """
        length: float = self.length()

        if length == 0:
            raise ZeroDivisionError('Cannot normalize a vector of zero length.')

        self.x /= length
        self.y /= length

    def is_normalized(self, precision: int = 4) -> bool:
        """
        Check whether the vector is normalized, i.e., its length is equal to one.

        :param precision: Precision to which the length of the vector is to be checked to keep a delta for
        floating-point inaccuracies; defaults to 4.
        :type precision: int

        :return: True if the length pr magnitude of the vector is equal to one; else False.
        :rtype: bool
        """
        return round(self.length(), precision) == 1

    def scale(self, other: Vector2D) -> None:
        """
        Scale the vector by another vector's corresponding components.

        :param other: Scaling factor vector.
        :type other: Vector2D
        """
        self.x *= other.x
        self.y *= other.y

    def as_tuple(self) -> tuple[float, float]:
        """
        Return the x and y components of the vector in a tuple. Beneficial for internal interoperability with Pygame.

        :return: Tuple of the vector's x and y component respectively.
        :rtype: tuple[float, float]
        """
        return self.x, self.y


def clamp(vector: Vector2D, min_: Vector2D, max_: Vector2D) -> Vector2D:
    """
    Clamp a vector between a specified minimum and maximum bound.

    :param vector: Vector to be clamped.
    :type vector: Vector2D
    :param min_: Minimum bound of the clamp.
    :type min_: Vector2D
    :param max_: Maximum bound of the clamp.
    :type max_: Vector2D

    :return: Vector clamped to the minimum and maximum bound.
    :rtype: Vector2D

    :raises ValueError: The maximum bound cannot be greater than the minimum bound on either component axis.
    """
    if min_.x > max_.x or min_.y > max_.y:
        raise ValueError('The minimum bound vector cannot be greater than the maximum bound vector.')

    clamped_vector = Vector2D(0, 0)

    # Clamp along the x-axis.
    if vector.x < min_.x:
        clamped_vector.x = min_.x
    elif vector.x > max_.x:
        clamped_vector.x = max_.x
    else:
        clamped_vector.x = vector.x

    # Clamp along the y-axis.
    if vector.y < min_.y:
        clamped_vector.y = min_.y
    elif vector.y > max_.y:
        clamped_vector.y = max_.y
    else:
        clamped_vector.y = vector.y

    return clamped_vector


def normalized(vector: Vector2D) -> Vector2D:
    """
    Normalize a vector, i.e., set its length to one while maintaining the same direction and return it.

    :param vector: Vector to be normalized.
    :type vector: Vector2D

    :return: Normalized vector of length or magnitude of one.
    :rtype: Vector2D

    :raises ZeroDivisionError: A vector of zero length cannot be normalized.
    """
    length: float = vector.length()

    if length == 0:
        raise ZeroDivisionError('Cannot normalize a vector of zero length.')

    vector.x /= length
    vector.y /= length

    return vector


def angle(from_vector: Vector2D, to_vector: Vector2D) -> float:
    """
    Calculate the unsigned angle between one vector and another. The unsigned angle means that the direction of
    rotation becomes irrelevant.

    :param from_vector: Initial vector from which the angle is measured.
    :type from_vector: Vector2D
    :param to_vector: Final vector from which the angle is stopped being measured.
    :type to_vector: Vector2D

    :return: Unsigned angle between the two vectors in radians.
    :rtype: float
    """
    if from_vector == to_vector:
        return 0

    return math.acos(dot(from_vector, to_vector) / (from_vector.length() * to_vector.length()))


def lerp(from_vector: Vector2D, to_vector: Vector2D, t: float) -> Vector2D:
    """
    Compute a smooth linear interpolation of a vector along both axes with respect to a constraint.

    :param from_vector: Initial vector for the interpolation.
    :type from_vector: Vector2D
    :param to_vector: Final vector for the interpolation.
    :type to_vector: Vector2D
    :param t: Interpolation parameter to smoothly go from the initial to final vector.
    :type t: float

    :return: Linearly interpolated vector between the initial and final vectors.
    :rtype: Vector2D
    """
    return from_vector + (to_vector - from_vector) * t


def dot(vector1: Vector2D, vector2: Vector2D) -> float:
    """
    Compute the dot product of two vectors.

    :param vector1: First vector.
    :type vector1: Vector2D
    :param vector2: Second vector.
    :type vector2: Vector2D

    :return: Dot or scalar product of the two vectors.
    :rtype: float
    """
    return vector1.x * vector2.x + vector1.y * vector2.y


def cross(vector1: Vector2D, vector2: Vector2D) -> float:
    """
    Compute the cross product of two vectors.

    :param vector1: First vector.
    :type vector1: Vector2D
    :param vector2: Second vector.
    :type vector2: Vector2D

    :return: Magnitude of the cross or vector product of the two vectors.
    :rtype: float
    """
    return vector1.x * vector2.y - vector1.y * vector2.x


def distance_between(vector1: Vector2D, vector2: Vector2D) -> float:
    """
    Compute the distance between two vectors.

    :param vector1: First vector.
    :type vector1: Vector2D
    :param vector2: Second vector.
    :type vector2: Vector2D

    :return: Distance between the two vectors.
    :rtype: float
    """
    return math.sqrt((vector1.x - vector2.x) ** 2 + (vector1.y - vector2.y) ** 2)


def distance_squared_between(vector1: Vector2D, vector2: Vector2D) -> float:
    """
    Compute the square of the distance between two vectors. Faster due to lack of a square root operation.

    :param vector1: First vector.
    :type vector1: Vector2D
    :param vector2: Second vector.
    :type vector2: Vector2D

    :return: Square of the distance between the two vectors.
    :rtype: float
    """
    return (vector1.x - vector2.x) ** 2 + (vector1.y - vector2.y) ** 2


def reflect(direction: Vector2D, normal: Vector2D) -> Vector2D:
    """
    Reflect a vector along a given normal to the direction of the vector.

    :param direction: Vector to be reflected.
    :type direction: Vector2D
    :param normal: Normal to the reflection.
    :type normal: Vector2D

    :return: Reflected vector with respect to the normal.
    :rtype: Vector2D

    :raises ValueError: The normal vector must be normalized, or have a length or magnitude of one.
    """
    if not normal.is_normalized():
        raise ValueError('The normal vector for reflection must be normalised, or naturally have a unit length.')

    return (normal * -2 * dot(direction, normal)) + direction


def from_tuple(position: tuple[float, float]) -> Vector2D:
    """
    Create a new vector using an existing tuple of components. Beneficial for internal interoperability with Pygame.

    :param position: Tuple of the vector's x and y component respectively.
    :type position: tuple[float, float]

    :return: Vector created from the tuple.
    :rtype: Vector2D
    """
    return Vector2D(*position)


def zero() -> Vector2D:
    """
    Create a new zero vector, i.e., x: 0, y: 0.

    :return: New zero vector.
    :rtype: Vector2D
    """
    return Vector2D(0, 0)


def one() -> Vector2D:
    """
    Create a new one vector: i.e., x: 1, y: 1.

    :return: New one vector.
    :rtype: Vector2D
    """
    return Vector2D(1, 1)


def up() -> Vector2D:
    """
    Create a new vector pointing in the up direction, i.e., x: 0, y: -1.

    :return: New up vector.
    :rtype: Vector2D
    """
    return Vector2D(0, -1)


def down() -> Vector2D:
    """
    Create a new vector pointing in the down direction, i.e., x: 0, y: 1.

    :return: New down vector.
    :rtype: Vector2D
    """
    return Vector2D(0, 1)


def left() -> Vector2D:
    """
    Create a new vector pointing in the left direction, i.e., x: -1, y: 0.

    :return: New left vector.
    :rtype: Vector2D
    """
    return Vector2D(-1, 0)


def right() -> Vector2D:
    """
    Create a new vector pointing in the right direction, i.e., x: 1, y: 0.

    :return: New right vector.
    :rtype: Vector2D
    """
    return Vector2D(1, 0)


def random() -> Vector2D:
    """
    Create a new vector pointing in a random direction, i.e. x: -1 | 0 | 1, y: -1 | 0 | 1.

    :return: New random vector.
    :rtype: Vector2D
    """
    return Vector2D(*rand.choices((-1, 0, 1), k=2))
