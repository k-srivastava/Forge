"""
Two-dimensional vectors in Forge.
"""
import math
import random as rand
from dataclasses import dataclass
from typing import Optional, Self, SupportsIndex, overload

import pygame

import forge.core.utils.math as forge_math
from forge.core.utils.exceptions import ClampError


@dataclass(slots=True)
class Vector2D:
    """
    Forge's representation of a two-dimensional vector.
    """
    x: float
    y: float

    def __add__(self, other: Self) -> Self:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y

        return self

    def __sub__(self, other: Self) -> Self:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y

        return self

    def __mul__(self, scalar: int | float) -> Self:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int | float) -> Self:
        return Vector2D(self.x * scalar, self.y * scalar)

    def __imul__(self, scalar: int | float) -> Self:
        self.x *= scalar
        self.y *= scalar

        return self

    def __truediv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        return Vector2D(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        self.x /= scalar
        self.y /= scalar

        return self

    def __floordiv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        return Vector2D(self.x // scalar, self.y // scalar)

    def __ifloordiv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        self.x //= scalar
        self.y //= scalar

        return self

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Self) -> bool:
        return self.x != other.x or self.y != other.y

    def __abs__(self) -> Self:
        return Vector2D(abs(self.x), abs(self.y))

    def __neg__(self) -> Self:
        return Vector2D(-self.x, -self.y)

    def __bool__(self) -> bool:
        return self.x != 0 and self.y != 0

    def __copy__(self) -> Self:
        return Vector2D(self.x, self.y)

    def __round__(self, n: Optional[SupportsIndex]) -> Self:
        return Vector2D(round(self.x, n), round(self.y, n))

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

        :return: True if the length or magnitude of the vector is equal to one; else False.
        :rtype: bool
        """
        return round(self.length(), precision) == 1

    def reflect(self, normal: Self) -> None:
        """
        Reflect the vector along a given normal to the direction of the vector.

        :param normal: Normal to the reflection.
        :type normal: Vector2D

        :raises ValueError: The normal vector must be normalized, or have a length or magnitude of one.
        """
        if not normal.is_normalized():
            raise ValueError('The normal vector for reflection must be normalised, or naturally have a unit length.')

        reflected_vector: Self = (normal * -2 * dot(self, normal)) + self
        self.x = reflected_vector.x
        self.y = reflected_vector.y

    def as_tuple(self) -> tuple[float, float]:
        """
        Return the x and y components of the vector in a tuple. Beneficial for internal interoperability with Pygame.

        :return: Tuple of the vector's x and y components respectively.
        :rtype: tuple[float, float]
        """
        return self.x, self.y

    def as_pygame_vector(self) -> pygame.math.Vector2:
        """
        Return the vector as a Pygame 2D vector. Beneficial for internal interoperability with Pygame.

        :return: Pygame vector from the vector's x and y components respectively.
        :rtype: pygame.math.Vector2
        """
        return pygame.math.Vector2(self.x, self.y)

    @classmethod
    def zero(cls) -> Self:
        """
        Create a new zero vector.

        :return: Zero vector.
        :rtype: Vector2D
        """
        return Vector2D(0, 0)

    @classmethod
    def one(cls) -> Self:
        """
        Create a new one vector; i.e., all components are 1.

        :return: One vector.
        :rtype: Vector3D
        """
        return Vector2D(1, 1)

    @classmethod
    def up(cls) -> Self:
        """
        Create a new vector pointing up; i.e., y = -1.

        :return: Up vector.
        :rtype: Vector2D
        """
        return Vector2D(0, -1)

    @classmethod
    def down(cls) -> Self:
        """
        Create a new vector pointing down; i.e., y = 1.

        :return: Down vector.
        :rtype: Vector2D
        """
        return Vector2D(0, 1)

    @classmethod
    def left(cls) -> Self:
        """
        Create a new vector pointing left; i.e., x = -1.

        :return: Left vector.
        :rtype: Vector2D
        """
        return Vector2D(-1, 0)

    @classmethod
    def right(cls) -> Self:
        """
        Create a new vector pointing right; i.e., x = 1.

        :return: Right vector.
        :rtype: Vector2D
        """
        return Vector2D(1, 0)

    @classmethod
    def random(cls, allow_zero_length: bool = True) -> Self:
        """
        Create a new vector pointing in a random direction, i.e. x: -1 | 0 | 1, y: -1 | 0 | 1.

        :param allow_zero_length: Allow a zero vector through random generation.
        :type allow_zero_length: bool

        :return: New random vector.
        :rtype: Vector2D
        """
        if allow_zero_length:
            return Vector2D(*rand.choices((-1, 0, 1), k=2))

        else:
            while True:
                random_vector = Vector2D(*rand.choices((-1, 0, 1), k=2))

                if random_vector.length_squared() != 0:
                    return random_vector


@dataclass(slots=True)
class Vector3D:
    """Forge's representation of a three-dimensional vector."""
    x: float
    y: float
    z: float

    def __add__(self, other: Self) -> Self:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Self) -> Self:
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other: Self) -> Self:
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Self) -> Self:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def __mul__(self, scalar: int | float) -> Self:
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: int | float) -> Self:
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __imul__(self, scalar: int | float) -> Self:
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

        return self

    def __truediv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __itruediv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        self.x /= scalar
        self.y /= scalar
        self.z /= scalar

        return self

    def __floordiv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        return Vector3D(self.x // scalar, self.y // scalar, self.z // scalar)

    def __ifloordiv__(self, scalar: int | float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        self.x //= scalar
        self.y //= scalar
        self.z //= scalar

        return self

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: Self) -> bool:
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __abs__(self) -> Self:
        return Vector3D(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self) -> Self:
        return Vector3D(-self.x, -self.y, -self.z)

    def __bool__(self) -> bool:
        return self.x != 0 and self.y != 0 and self.z != 0

    def __copy__(self) -> Self:
        return Vector3D(self.x, self.y, self.z)

    def __round__(self, n: Optional[SupportsIndex]) -> Self:
        return Vector3D(round(self.x, n), round(self.y, n), round(self.z, n))

    def length(self) -> float:
        """
        Compute the length of the vector.

        :return: Length or magnitude of the vector.
        :rtype: float
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def length_squared(self) -> float:
        """
        Compute the square of the length of the vector. Faster due to lack of a square root operation.

        :return: Square of the length or magnitude of the vector.
        :rtype: float
        """
        return self.x ** 2 + self.y ** 2 + self.z ** 2

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
        self.z /= length

    def is_normalized(self, precision: int = 4) -> bool:
        """
        Check whether the vector is normalized, i.e., its length is equal to one.

        :param precision: Precision to which the length of the vector is to be checked to keep a delta for
                          floating-point inaccuracies; defaults to 4.
        :type precision: int

        :return: True if the length or magnitude of the vector is equal to one; else False.
        :rtype: bool
        """
        return round(self.length(), precision) == 1

    def reflect(self, normal: Self) -> None:
        """
        Reflect the vector along a given normal to the direction of the vector.

        :param normal: Normal to the reflection.
        :type normal: Vector3D

        :raises ValueError: The normal vector must be normalized, or have a length or magnitude of one.
        """
        if not normal.is_normalized():
            raise ValueError('The normal vector for reflection must be normalised, or naturally have a unit length.')

        reflected_vector: Self = (normal * -2 * dot(self, normal)) + self
        self.x = reflected_vector.x
        self.y = reflected_vector.y
        self.z = reflected_vector.z

    def as_tuple(self) -> tuple[float, float, float]:
        """
        Return the x and y components of the vector in a tuple. Beneficial for internal interoperability with Pygame.

        :return: Tuple of the vector's x, y and z components respectively.
        :rtype: tuple[float, float, float]
        """
        return self.x, self.y, self.z

    def as_pygame_vector(self) -> pygame.math.Vector3:
        """
        Return the vector as a Pygame 2D vector. Beneficial for internal interoperability with Pygame.

        :return: Pygame vector from the vector's x, y and z components respectively.
        :rtype: pygame.math.Vector3
        """
        return pygame.math.Vector3(self.x, self.y, self.z)

    @classmethod
    def zero(cls) -> Self:
        """
        Create a new zero vector.

        :return: Zero vector.
        :rtype: Vector3D
        """
        return Vector3D(0, 0, 0)

    @classmethod
    def one(cls) -> Self:
        """
        Create a new one vector; i.e., all components are 1.

        :return: One vector.
        :rtype: Vector3D
        """
        return Vector3D(1, 1, 1)

    @classmethod
    def up(cls) -> Self:
        """
        Create a new vector pointing up; i.e., y = -1.

        :return: Up vector.
        :rtype: Vector3D
        """
        return Vector3D(0, -1, 0)

    @classmethod
    def down(cls) -> Self:
        """
        Create a new vector pointing down; i.e., y = 1.

        :return: Down vector.
        :rtype: Vector3D
        """
        return Vector3D(0, 1, 0)

    @classmethod
    def left(cls) -> Self:
        """
        Create a new vector pointing left; i.e., x = -1.

        :return: Left vector.
        :rtype: Vector3D
        """
        return Vector3D(-1, 0, 0)

    @classmethod
    def right(cls) -> Self:
        """
        Create a new vector pointing right; i.e., x = 1.

        :return: Right vector.
        :rtype: Vector3D
        """
        return Vector3D(1, 0, 0)

    @classmethod
    def forward(cls) -> Self:
        """
        Create a new vector pointing forward; i.e., z = -1.

        :return: Forward vector.
        :rtype: Vector3D
        """
        return Vector3D(0, 0, -1)

    @classmethod
    def backward(cls) -> Self:
        """
        Create a new vector pointing backward; i.e., z = 1.

        :return: Backward vector.
        :rtype: Vector3D
        """
        return Vector3D(0, 0, 1)

    @classmethod
    def random(cls, allow_zero_length: bool = True) -> Self:
        """
        Create a new vector pointing in a random direction, i.e. x: -1 | 0 | 1, y: -1 | 0 | 1, z: -1 | 0 | 1.

        :param allow_zero_length: Allow a zero vector through random generation.
        :type allow_zero_length: bool

        :return: New random vector.
        :rtype: Vector3D
        """
        if allow_zero_length:
            return Vector3D(*rand.choices((-1, 0, 1), k=3))

        else:
            while True:
                random_vector = Vector3D(*rand.choices((-1, 0, 1), k=3))

                if random_vector.length_squared() != 0:
                    return random_vector


@overload
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

    :raises ClampError: The maximum bound cannot be greater than the minimum bound on either component axis.
    """


@overload
def clamp(vector: Vector3D, min_: Vector3D, max_: Vector3D) -> Vector3D:
    """
    Clamp a vector between a specified minimum and maximum bound.

    :param vector: Vector to be clamped.
    :type vector: Vector3D
    :param min_: Minimum bound of the clamp.
    :type min_: Vector3D
    :param max_: Maximum bound of the clamp.
    :type max_: Vector3D

    :return: Vector clamped to the minimum and maximum bound.
    :rtype: Vector3D

    :raises ClampError: The maximum bound cannot be greater than the minimum bound on any component axis.
    """


def clamp(vector, min_, max_):
    if type(vector) is Vector2D:
        if min_.x > max_.x or min_.y > max_.y:
            raise ClampError()

        return Vector2D(
            forge_math.clamp(vector.x, min_.x, max_.x),
            forge_math.clamp(vector.y, min_.y, max_.y)
        )

    if type(vector) is Vector3D:
        if min_.x > max_.x or min_.y > max_.y or min_.z > max_.z:
            raise ClampError()

        return Vector3D(
            forge_math.clamp(vector.x, min_.x, max_.x),
            forge_math.clamp(vector.y, min_.y, max_.y),
            forge_math.clamp(vector.y, min_.y, max_.y)
        )

    raise TypeError(f'Cannot clamp a {type(vector)} between two vectors.')


@overload
def normalized(vector: Vector2D) -> Vector2D:
    """
    Normalize a vector, i.e., set its length to one while maintaining the same direction and return it.

    :param vector: Vector to be normalized.
    :type vector: Vector2D

    :return: The normalized vector of length or magnitude of one.
    :rtype: Vector2D

    :raises ZeroDivisionError: A vector of zero length cannot be normalized.
    """


@overload
def normalized(vector: Vector3D) -> Vector3D:
    """
    Normalize a vector, i.e., set its length to one while maintaining the same direction and return it.

    :param vector: Vector to be normalized.
    :type vector: Vector2D

    :return: The normalized vector of length or magnitude of one.
    :rtype: Vector2D

    :raises ZeroDivisionError: A vector of zero length cannot be normalized.
    """


def normalized(vector):
    length: float = vector.length()

    if length == 0:
        raise ZeroDivisionError('Cannot normalize a vector of zero length.')

    vector.x /= length
    vector.y /= length

    if type(vector) is Vector3D:
        vector.z /= length

    return vector


@overload
def scaled(vector: Vector2D, new_scale: float) -> Vector2D:
    """
    Scale a vector to a given length while maintaining its current direction.

    :param vector: Vector to be scaled.
    :type vector: Vector2D
    :param new_scale: New length of the vector.
    :type new_scale: float

    :return: The scaled vector with the given length and same direction.
    :rtype: Vector2D
    """


@overload
def scaled(vector: Vector3D, new_scale: float) -> Vector3D:
    """
    Scale a vector to a given length while maintaining its current direction.

    :param vector: Vector to be scaled.
    :type vector: Vector3D
    :param new_scale: New length of the vector.
    :type new_scale: float

    :return: The scaled vector with the given length and same direction.
    :rtype: Vector3D
    """


def scaled(vector, new_scale):
    return normalized(vector) * new_scale


@overload
def angle(from_vector: Vector2D, to_vector: Vector2D) -> float:
    """
    Calculate the unsigned angle between one vector and another. The unsigned angle means that the direction of
    rotation becomes irrelevant.

    :param from_vector: Initial vector from which the angle is measured.
    :type from_vector: Vector2D
    :param to_vector: Final vector from which the angle is stopped being measured.
    :type to_vector: Vector2D

    :return: The unsigned angle between the two vectors in radians.
    :rtype: float
    """


@overload
def angle(from_vector: Vector3D, to_vector: Vector3D) -> float:
    """
    Calculate the unsigned angle between one vector and another. The unsigned angle means that the direction of
    rotation becomes irrelevant.

    :param from_vector: Initial vector from which the angle is measured.
    :type from_vector: Vector3D
    :param to_vector: Final vector from which the angle is stopped being measured.
    :type to_vector: Vector3D

    :return: The unsigned angle between the two vectors in radians.
    :rtype: float
    """


def angle(from_vector, to_vector):
    if from_vector == to_vector:
        return 0.0

    return math.acos(dot(from_vector, to_vector) / (from_vector.length() * to_vector.length()))


@overload
def lerp(from_vector: Vector2D, to_vector: Vector2D, t: float) -> Vector2D:
    """
    Compute a smooth linear interpolation of a vector along both axes with respect to a constraint.

    :param from_vector: Initial vector for the interpolation.
    :type from_vector: Vector2D
    :param to_vector: Final vector for the interpolation.
    :type to_vector: Vector2D
    :param t: Interpolation parameter to smoothly go from the initial to final vector.
    :type t: float

    :return: The linearly interpolated vector between the initial and final vectors.
    :rtype: Vector2D
    """


@overload
def lerp(from_vector: Vector3D, to_vector: Vector3D, t: float) -> Vector3D:
    """
    Compute a smooth linear interpolation of a vector along both axes with respect to a constraint.

    :param from_vector: Initial vector for the interpolation.
    :type from_vector: Vector3D
    :param to_vector: Final vector for the interpolation.
    :type to_vector: Vector3D
    :param t: Interpolation parameter to smoothly go from the initial to final vector.
    :type t: float

    :return: The linearly interpolated vector between the initial and final vectors.
    :rtype: Vector3D
    """


def lerp(from_vector, to_vector, t):
    return from_vector + (to_vector - from_vector) * t


@overload
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


@overload
def dot(vector1: Vector3D, vector2: Vector3D) -> float:
    """
    Compute the dot product of two vectors.

    :param vector1: First vector.
    :type vector1: Vector3D
    :param vector2: Second vector.
    :type vector2: Vector3D

    :return: Dot or scalar product of the two vectors.
    :rtype: float
    """


def dot(vector1, vector2):
    result = vector1.x * vector2.x + vector1.y * vector2.y

    if type(vector1) is not type(vector2):
        raise TypeError(f'Cannot calculate dot product of {type(vector1)} and {type(vector2)}.')

    if type(vector1) is Vector3D:
        result += vector1.z * vector2.z

    return result


@overload
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


@overload
def cross(vector1: Vector3D, vector2: Vector3D) -> float:
    """
    Compute the cross product of two vectors.

    :param vector1: First vector.
    :type vector1: Vector3D
    :param vector2: Second vector.
    :type vector2: Vector3D

    :return: Magnitude of the cross or vector product of the two vectors.
    :rtype: float
    """


def cross(vector1, vector2):
    if type(vector1) is Vector2D and type(vector2) is Vector2D:
        return vector1.x * vector2.y - vector1.y * vector2.x

    if type(vector1) is Vector3D and type(vector2) is Vector3D:
        cross_x = vector1.y * vector2.z - vector1.z * vector2.y
        cross_y = vector1.z * vector2.x - vector1.x * vector2.z
        cross_z = vector1.x * vector2.y - vector1.y * vector2.x

        return Vector3D(cross_x, cross_y, cross_z).length()

    raise TypeError(f'Cannot calculate cross product of {type(vector1)} and {type(vector2)}.')


@overload
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


@overload
def distance_between(vector1: Vector3D, vector2: Vector3D) -> float:
    """
    Compute the distance between two vectors.

    :param vector1: First vector.
    :type vector1: Vector3D
    :param vector2: Second vector.
    :type vector2: Vector3D

    :return: Distance between the two vectors.
    :rtype: float
    """


def distance_between(vector1, vector2):
    if type(vector1) is Vector2D and type(vector2) is Vector2D:
        return math.sqrt((vector1.x - vector2.x) ** 2 + (vector1.y - vector2.y) ** 2)

    if type(vector1) is Vector3D and type(vector2) is Vector3D:
        return math.sqrt((vector1.x - vector2.x) ** 2 + (vector1.y - vector2.y) ** 2 + (vector1.z - vector2.z) ** 2)

    raise TypeError(f'Cannot calculate distance between {type(vector1)} and {type(vector2)}.')


@overload
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


@overload
def distance_squared_between(vector1: Vector3D, vector2: Vector3D) -> float:
    """
    Compute the square of the distance between two vectors. Faster due to lack of a square root operation.

    :param vector1: First vector.
    :type vector1: Vector3D
    :param vector2: Second vector.
    :type vector2: Vector3D

    :return: Square of the distance between the two vectors.
    :rtype: float
    """


def distance_squared_between(vector1, vector2):
    if type(vector1) is Vector2D and type(vector2) is Vector2D:
        return (vector1.x - vector2.x) ** 2 + (vector1.y - vector2.y) ** 2

    if type(vector1) is Vector3D and type(vector2) is Vector3D:
        return (vector1.x - vector2.x) ** 2 + (vector1.y - vector2.y) ** 2 + (vector1.z - vector2.z) ** 2

    raise TypeError(f'Cannot calculate squared distance between {type(vector1)} and {type(vector2)}.')


@overload
def reflect_to(direction: Vector2D, normal: Vector2D) -> Vector2D:
    """
    Reflect a vector along a given normal to the direction of the vector.

    :param direction: Vector to be reflected.
    :type direction: Vector2D
    :param normal: Normal to the reflection.
    :type normal: Vector2D

    :return: The reflected vector with respect to the normal.
    :rtype: Vector2D

    :raises ValueError: The normal vector must be normalized, or have a length or magnitude of one.
    """


@overload
def reflect_to(direction: Vector3D, normal: Vector3D) -> Vector3D:
    """
    Reflect a vector along a given normal to the direction of the vector.

    :param direction: Vector to be reflected.
    :type direction: Vector3D
    :param normal: Normal to the reflection.
    :type normal: Vector3D

    :return: The reflected vector with respect to the normal.
    :rtype: Vector3D

    :raises ValueError: The normal vector must be normalized, or have a length or magnitude of one.
    """


def reflect_to(direction, normal):
    if not normal.is_normalized():
        raise ValueError('The normal vector for reflection must be normalised, or naturally have a unit length.')

    return (normal * -2 * dot(direction, normal)) + direction


@overload
def from_tuple(position: tuple[float, float]) -> Vector2D:
    """
    Create a new vector using an existing tuple of components. Beneficial for internal interoperability with Pygame.

    :param position: Tuple of the vector's x and y components respectively.
    :type position: tuple[float, float]

    :return: Vector created from the tuple.
    :rtype: Vector2D
    """


@overload
def from_tuple(position: tuple[float, float, float]) -> Vector3D:
    """
    Create a new vector using an existing tuple of components. Beneficial for internal interoperability with Pygame.

    :param position: Tuple of the vector's x, y and z components respectively.
    :type position: tuple[float, float, float]

    :return: Vector created from the tuple.
    :rtype: Vector3D
    """


def from_tuple(position):
    if len(position) == 2:
        return Vector2D(*position)

    if len(position) == 3:
        return Vector3D(*position)

    raise ValueError(f'Cannot create a vector with {len(position)} coordinates.')


@overload
def from_pygame_vector(vector: pygame.math.Vector2) -> Vector2D:
    """
    Create a new vectory using an existing Pygame vector. Beneficial for internal interoperability with Pygame.

    :param vector: Pygame 2D vector.
    :type vector: pygame.math.Vector2

    :return: Forge vector created from the Pygame vector.
    :rtype: Vector2D
    """


@overload
def from_pygame_vector(vector: pygame.math.Vector3) -> Vector3D:
    """
    Create a new vectory using an existing Pygame vector. Beneficial for internal interoperability with Pygame.

    :param vector: Pygame 3D vector.
    :type vector: pygame.math.Vector3

    :return: Forge vector created from the Pygame vector.
    :rtype: Vector3D
    """


def from_pygame_vector(vector):
    if type(vector) is pygame.math.Vector2:
        return Vector2D(vector.x, vector.y)

    if type(vector) is pygame.math.Vector3:
        return Vector3D(vector.x, vector.y, vector.z)

    raise TypeError(f'Cannot create a Forge vector form {type(vector)}.')
