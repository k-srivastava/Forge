"""Shapes used throughout Hearth."""
from copy import copy
from enum import IntEnum, auto
from functools import cached_property
from math import pi
from typing import Optional

import pygame

from forge.core.engine.color import Color
from forge.core.physics import vector
from forge.core.physics.vector import Vector2D
from forge.core.utils.aliases import Surface
from forge.hearth.elements.base import Shape, UIElement
from forge.hearth.elements.border import Border


class ShapeType(IntEnum):
    """Enumeration of shapes supported by Hearth."""
    RECTANGLE = auto()
    CIRCLE = auto()
    POLYGON = auto()


class Line(UIElement):
    """Basic lines in Hearth."""
    __slots__ = 'start_point', 'end_point', 'width'

    def __init__(
            self, start_point: Vector2D, end_point: Vector2D, color: Color,
            parent: Optional[UIElement | Shape] = None, width: int = 1
    ) -> None:
        """
        Initialize the line.

        :param start_point: Starting point of the line.
        :type start_point: Vector2D
        :param end_point: Ending point of the line.
        :type end_point: Vector2D
        :param color: Color of the line.
        :type color: Color
        :param parent: Parent of the line; defaults to None.
        :type parent: Optional[UIElement | Shape]
        :param width: Width of the line; defaults to 1.
        :type width: int
        """
        self.start_point = start_point
        self.end_point = end_point
        self.width = width

        super().__init__(color, parent)

    @property
    def top_left(self) -> Vector2D:
        """
        Top-left of the line.

        :return: Top-left of the line.
        :rtype: Vector2D
        """
        return Vector2D(min(self.start_point.x, self.end_point.x), min(self.start_point.y, self.end_point.y))

    @property
    def center(self) -> Vector2D:
        """
        Center of the line.

        :return: Center of the line.
        :rtype: Vector2D
        """
        return (self.start_point + self.end_point) / 2

    @property
    def length(self) -> float:
        """
        Length of the line.

        :return: Length of the line.
        :rtype: float
        """
        return vector.distance_between(self.start_point, self.end_point)

    @property
    def length_squared(self) -> float:
        """
        Square of the length of the line. Faster due to lack of a square root operation.

        :return: Square of the length of the line.
        :rtype: float
        """
        return vector.distance_squared_between(self.start_point, self.end_point)

    def render(self, display: Surface) -> None:
        """
        Render the line to the display.

        :param display: Display to which the line is to be rendered.
        :type display: Surface
        """
        pygame.draw.line(
            display, self.color.as_tuple(), self.start_point.as_tuple(), self.end_point.as_tuple(),
            self.width
        )

        super().render(display)

    def as_tuples(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """
        Return the start and end points of the line as tuples. Beneficial for internal interoperability with Pygame.

        :return: Tuple of the start and end points' x and y components respectively.
        :rtype: tuple[tuple[float, float], tuple[float, float]]
        """
        return self.start_point.as_tuple(), self.end_point.as_tuple()

    def as_pygame_vectors(self) -> tuple[pygame.math.Vector2, pygame.math.Vector2]:
        """
        Return the start and end points of the line as Pygame vectors. Beneficial for internal interoperability with
        Pygame.

        :return: Tuple of the start and end points as Pygame vectors.
        :rtype: tuple[pygame.math.Vector2, pygame.math.Vector2]
        """
        return self.start_point.as_pygame_vector(), self.end_point.as_pygame_vector()


class Rectangle(Shape):
    """Basic rectangles in Hearth."""
    __slots__ = 'width', 'height', 'corner_radius', '_top_left'

    def __init__(
            self, top_left: Vector2D, width: int, height: int, color: Color,
            parent: Optional[UIElement | Shape] = None, line_width: int = 0, corner_radius: Optional[int] = None,
            border: Optional[Border] = None
    ) -> None:
        """
        Initialize the rectangle.

        :param top_left: Top-left point of the rectangle.
        :type top_left: Vector2D
        :param width: Width of the rectangle.
        :type width: int
        :param height: Height of the rectangle.
        :type height: int
        :param color: Color of the rectangle.
        :type color: Color
        :param parent: Parent of the rectangle; defaults to None.
        :type parent: Optional[UIElement | Shape]
        :param line_width: Width of the line of the rectangle; defaults to 0 - solid rectangle.
        :type line_width: int
        :param corner_radius: Radii of the corners of the rectangle; defaults to None.
        :type corner_radius: Optional[int]
        :param border: Border of the rectangle; defaults to None.
        :type border: Optional[Border]

        :raises BodyAreaError: Size of the rectangle should be within the given body size constraints, if being checked.
        """
        self.width = width
        self.height = height
        self.corner_radius = corner_radius

        self._top_left = top_left

        super().__init__(color, line_width, border, parent)

    @property
    def top_left(self) -> Vector2D:
        """
        Getter for the top-left-most point of the rectangle.

        :return: Top-left-most point of the rectangle.
        :rtype: Vector2D
        """
        return self._top_left

    @top_left.setter
    def top_left(self, value: Vector2D) -> None:
        """
        Setter for the top-left-most point of the rectangle.

        :param value: New value of the top-left-most point of the rectangle.
        :type value: Vector2D
        """
        self._top_left = value

    @property
    def center(self) -> Vector2D:
        """
        Getter for the center point of the rectangle.

        :return: Center point of the rectangle.
        :rtype: Vector2D
        """
        return Vector2D(self.top_left.x + (self.width // 2), self.top_left.y + (self.height // 2))

    @center.setter
    def center(self, value: Vector2D) -> None:
        """
        Setter for the center point of the rectangle.

        :param value: New value of the center of the rectangle.
        :type value: Vector2D
        """
        self._top_left = Vector2D(value.x - self.width // 2, value.y - self.height // 2)

    @property
    def area(self) -> float:
        """
        Getter for the area of the rectangle.

        :return: Area of the rectangle.
        :rtype: float
        """
        return float(self.width * self.height)

    @property
    def perimeter(self) -> float:
        """
        Getter for the perimeter of the rectangle.

        :return: Perimeter of the rectangle.
        :rtype: float
        """
        return float((self.width + self.height) * 2)

    def computed_width(self) -> float:
        return self.width

    def computed_height(self) -> float:
        return self.height

    def vertices(self, clockwise: bool = True) -> tuple[Vector2D, Vector2D, Vector2D, Vector2D]:
        """
        Retrieve the vertices of the rectangle.

        :param clockwise: Whether to get the vertices in clockwise or counter-clockwise order; defaults to True.
        :type clockwise: bool

        :return: All the vertices of the rectangle.
        :rtype: tuple[Vector2D, Vector2D, Vector2D, Vector2D]
        """
        top_left = copy(self._top_left)
        top_right = Vector2D(self._top_left.x + self.width, self._top_left.y)
        bottom_left = Vector2D(self._top_left.x, self._top_left.y + self.height)
        bottom_right = Vector2D(self._top_left.x + self.width, self._top_left.y + self.height)

        if clockwise:
            return top_left, top_right, bottom_right, bottom_left

        return top_left, bottom_left, bottom_right, top_right

    def render(self, display: Surface) -> None:
        """
        Render the rectangle to the display.

        :param display: Display to which the rectangle is to be rendered.
        :type display: Surface
        """
        pygame.draw.rect(
            display, self.color.as_tuple(), self.as_pygame_rect(), self.line_width,
            self.corner_radius if self.corner_radius is not None else -1
        )

        if self.border is not None:
            pygame.draw.rect(
                display, self.border.color.as_tuple(), self.as_pygame_rect(), self.border.width,
                self.border.radius if self.border.radius is not None else -1
            )

        super().render(display)

    def as_pygame_rect(self) -> pygame.rect.Rect:
        """
        Return the vertices of the rectangle as a Pygame rect. Beneficial for interoperability with Pygame.

        :return: Pygame rect bounds of the rectangle.
        :rtype: pygame.rect.Rect
        """
        return pygame.rect.Rect(self.top_left.x, self.top_left.y, self.width, self.height)


class Circle(Shape):
    """Basic circles in Hearth."""
    __slots__ = 'radius', 'line_width'

    def __init__(
            self, center: Vector2D, radius: int, color: Color, parent: Optional[UIElement | Shape] = None,
            line_width: int = 0, border: Optional[Border] = None
    ) -> None:
        """
        Initialize the circle.

        :param center: Center of the circle.
        :type center: Vector2D
        :param radius: Radius of the circle.
        :type radius: int
        :param color: Color of the circle.
        :type color: Color
        :param parent: Parent of the circle; defaults to None.
        :type parent: Optional[UIElement | Shape]
        :param line_width: Width of the line of the circle; defaults to 0 - solid circle.
        :type line_width: int
        :param border: Border of the circle; defaults to None.
        :type border: Optional[Border]

        :raises BodyAreaError: Size of the circle should be within the given body size constraints, if being checked.
        """
        self.radius = radius
        self._center = center

        super().__init__(color, line_width, border, parent)

    @property
    def top_left(self) -> Vector2D:
        """
        Getter for the top-left-most point of the circle.

        :return: Top-left-most point of the circle.
        :rtype: Vector2D
        """
        return self._center - Vector2D(self.radius, self.radius)

    @top_left.setter
    def top_left(self, value: Vector2D) -> None:
        """
        Setter for the top-left-most point of the circle.

        :param value: New value of the top-left-most point of the circle.
        :type value: Vector2D
        """
        self._center = value + Vector2D(self.radius, self.radius)

    @property
    def center(self) -> Vector2D:
        """
        Getter for the center point of the circle.

        :return: Center point of the circle.
        :rtype: Vector2D
        """
        return self._center

    @center.setter
    def center(self, value: Vector2D) -> None:
        """
        Setter for the center point of the circle.

        :param value: New value of the center of the circle.
        :type value: Vector2D
        """
        self._center = value

    @cached_property
    def area(self) -> float:
        """
        Getter for the area of the circle.

        :return: Area of the circle.
        :rtype: float
        """
        return pi * self.radius ** 2

    @cached_property
    def perimeter(self) -> float:
        """
        Getter for the perimeter of the circle.

        :return: Perimeter of the circle.
        :rtype: float
        """
        return 2 * pi * self.radius

    def computed_width(self) -> float:
        return self.radius * 2

    def computed_height(self) -> float:
        return self.radius * 2

    def render(self, display: Surface) -> None:
        """
        Render the circle to the display.

        :param display: Display to which the circle is to be rendered.
        :type display: Surface
        """
        pygame.draw.circle(
            display, self.color.as_tuple(), self.center.as_tuple(), self.radius, self.line_width
        )

        if self.border is not None:
            pygame.draw.circle(
                display, self.border.color.as_tuple(), self.center.as_tuple(), self.radius, self.border.width
            )

        super().render(display)


class Polygon(Shape):
    """Basic polygons in Hearth."""
    __slots__ = 'vertices'

    def __init__(
            self, vertices: list[Vector2D], color: Color, parent: Optional[UIElement | Shape] = None,
            line_width: int = 0, border: Optional[Border] = None
    ) -> None:
        """
        Initialize the polygon.

        :param vertices: Vertices of the polygon.
        :type vertices: list[Vector2D]
        :param color: Color of the polygon.
        :type color: Color
        :param parent: Parent of the polygon; defaults to None.
        :type parent: Optional[UIElement | Shape]
        :param line_width: Width of the polygon line; defaults to 0.
        :type line_width: int
        :param border: Border of the polygon; defaults to None.
        :type border: Optional[Border]
        """
        self.vertices = vertices
        super().__init__(color, line_width, border, parent)

    @property
    def top_left(self) -> Vector2D:
        """
        Getter for the top-left-most point of the polygon.

        :return: Top-left-most point of the polygon.
        :rtype: Vector2D
        """
        return Vector2D(min(vertex.x for vertex in self.vertices), min(vertex.y for vertex in self.vertices))

    @top_left.setter
    def top_left(self, value: Vector2D) -> None:
        """
        Setter for the top-left-most point of the polygon.

        :param value: New value of the top-left-most point of the polygon.
        :type value: Vector2D
        """
        displacement: Vector2D = value - self.top_left

        for vertex in self.vertices:
            vertex += displacement

    @property
    def center(self) -> Vector2D:
        """
        Getter for the center point of the polygon.

        :return: Center point of the polygon.
        :rtype: vector.Vector2D
        """
        total = Vector2D.zero()

        for vertex in self.vertices:
            total += vertex

        return total / len(self.vertices)

    @center.setter
    def center(self, value: Vector2D) -> None:
        """
        Setter for the center point of the polygon.

        :param value: New value of the center of the polygon.
        :type value: Vector2D
        """
        displacement: Vector2D = value - self.center

        for vertex in self.vertices:
            vertex += displacement

    @cached_property
    def area(self) -> float:
        """
        Getter for the area of the polygon.

        :return: Area of the polygon.
        :rtype: float
        """
        # TODO: Implement the area of a polygon.
        raise NotImplementedError('Area of the polygon not implemented.')

    @cached_property
    def perimeter(self) -> float:
        """
        Getter for the perimeter of the rectangle.

        :return: Perimeter of the rectangle.
        :rtype: float
        """
        length: float = 0

        for i in range(len(self.vertices) - 1):
            length += vector.distance_between(self.vertices[i], self.vertices[i + 1])

        length += vector.distance_between(self.vertices[-1], self.vertices[0])

        return length

    def computed_width(self) -> float:
        vertices_x = (vertex.x for vertex in self.vertices)
        return max(vertices_x) - min(vertices_x)

    def computed_height(self) -> float:
        vertices_y = (vertex.y for vertex in self.vertices)
        return max(vertices_y) - min(vertices_y)

    def render(self, display: Surface) -> None:
        """
        Render the polygon to the display.

        :param display: Display to which the polygon is to be rendered.
        :type display: Surface
        """

        pygame.draw.polygon(
            display, self.color.as_tuple(), [vertex.as_tuple() for vertex in self.vertices], self.line_width,
        )

        if self.border is not None:
            pygame.draw.polygon(
                display, self.border.color.as_tuple(), [vertex.as_tuple() for vertex in self.vertices],
                self.border.width
            )

        super().render(display)
