"""
Basic shapes in Forge.
"""
import dataclasses
import enum
import math
import typing


# A no-inspection has to be inserted because of a PyCharm bug.
# PyCharm displays erroneous warnings when using enum.auto().
# noinspection PyArgumentList
class ShapeType(enum.Enum):
    """
    Enumeration of all shape types supported by Forge.
    """
    RECTANGLE = enum.auto()
    CIRCLE = enum.auto()


@dataclasses.dataclass(slots=True)
class Shape(typing.Protocol):
    """
    Base shape class in Forge.
    """
    _shape_type: ShapeType = dataclasses.field(init=False)

    def area(self) -> float:
        """
        Calculate the area of the shape.

        :return: Area of the shape.
        :rtype: float
        """


@dataclasses.dataclass(slots=True)
class Rectangle(Shape):
    """
    Rectangle shape in Forge.
    """
    width: float
    height: float

    def __post_init__(self) -> None:
        """
        Set the internal shape type variable to a rectangle.
        """
        self._shape_type: ShapeType = ShapeType.RECTANGLE

    def area(self) -> float:
        """
        Calculate the area of the rectangle.

        :return: Area of the rectangle.
        :rtype: float
        """
        return self.width * self.height


@dataclasses.dataclass(slots=True)
class Circle(Shape):
    """
    Circle shape in Forge.
    """
    radius: float

    def __post_init__(self) -> None:
        """
        Set the internal shape type variable to a circle.
        """
        self._shape_type: ShapeType = ShapeType.CIRCLE

    def area(self) -> float:
        """
        Calculate the area of the circle.

        :return: Area of the circle.
        :rtype: float
        """
        return math.pi * (self.radius ** 2)
