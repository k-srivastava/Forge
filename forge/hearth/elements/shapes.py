"""
Shapes used throughout Hearth to create more complex UI elements.
"""
import copy
import dataclasses
import enum

import pygame

import forge.core.engine.color
import forge.core.engine.constants
import forge.core.engine.renderer
import forge.core.physics.vector
import forge.core.utils.aliases
import forge.core.utils.base
import forge.core.utils.id
import forge.hearth.elements.base
import forge.hearth.settings


# A no-inspection has to be inserted because of a PyCharm bug.
# PyCharm displays erroneous warnings when using enum.auto().
# noinspection PyArgumentList
class Shape(enum.Enum):
    """
    Enumeration of shapes supported by Hearth.
    """
    RECTANGLE = enum.auto()
    CIRCLE = enum.auto()
    POLYGON = enum.auto()


@dataclasses.dataclass(slots=True)
class Border:
    """
    Border for each supported shape in Hearth.
    """
    width: int
    color: forge.core.engine.color.Color
    radius: int | None = None  # A border radius is only applicable for rectangles.


class Line(forge.hearth.elements.base.UIElement):
    """
    Basic lines in Hearth.
    """

    __slots__ = 'start_point', 'end_point', 'parent', 'children', 'color', 'line_width', '_id'

    def __init__(
            self,
            start_point: forge.core.physics.vector.Vector2D,
            end_point: forge.core.physics.vector.Vector2D,
            color: forge.core.engine.color.Color,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 1,
    ) -> None:
        """
        Initialize the line.

        :param start_point: Starting point of the line.
        :type start_point: forge.core.physics.vector.Vector2D
        :param end_point: Ending point of the line.
        :type end_point: forge.core.physics.vector.Vector2D
        :param color: Color of the line.
        :type color: forge.core.engine.color.Color
        :param parent: Parent of the line; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the line; defaults to 1.
        :type line_width: int
        """
        self.start_point = start_point
        self.end_point = end_point
        self.parent = parent
        self.children = []

        self.color = color
        self.line_width = line_width

        self._id = forge.core.utils.id.generate_random_id()

        if self.parent is not None:
            self.parent.children.append(self)

            if forge.hearth.settings.NON_CONSTRAINED_CHILDREN_USE_RELATIVE_POSITIONING:
                calculate_relative_positions(self.parent, [self.start_point, self.end_point])

    @property
    def center(self) -> forge.core.physics.vector.Vector2D:
        """
        Calculate the center of the line.

        :return: Center of the line.
        :rtype: forge.core.physics.vector.Vector2D
        """
        return (self.start_point + self.end_point) / 2

    def id(self) -> int:
        """
        Get the unique ID of the line.

        :return: ID of the line.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the line to a renderer.

        :param renderer_name: Name of the renderer to which the line is to be added; defaults to the base UI renderer.
        :type renderer_name: str
        """
        forge.core.engine.renderer.get_renderer_from_name(renderer_name).elements.append(self)

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the line to the display.

        :param display: Display to which the line is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        pygame.draw.line(
            display,
            self.color.as_pygame_color(),
            self.start_point.as_tuple(), self.end_point.as_tuple(),
            self.line_width
        )

        if forge.hearth.settings.AUTO_RENDER_CHILDREN:
            for child in self.children:
                child.render(display)

    def update(self) -> None:
        """
        Update the line.
        """
        if forge.hearth.settings.AUTO_UPDATE_CHILDREN:
            for child in self.children:
                child.update()

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


class Rectangle(forge.hearth.elements.base.UIElement):
    """
    Basic rectangles in Hearth.
    """

    __slots__ = (
        'top_left', 'width', 'height', 'parent', 'children', 'color', 'line_width', 'corner_radius', 'border', '_id'
    )

    def __init__(
            self,
            top_left: forge.core.physics.vector.Vector2D, width: int, height: int,
            color: forge.core.engine.color.Color,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            corner_radius: int | None = None,
            border: Border | None = None
    ) -> None:
        """
        Initialize the rectangle.

        :param top_left: Top left point of the rectangle.
        :type top_left: forge.core.physics.vector.Vector2D
        :param width: Width of the rectangle.
        :type width: int
        :param height: Height of the rectangle.
        :type height: int
        :param color: Color of thr rectangle.
        :type color: forge.core.engine.color.Color
        :param parent: Parent of the rectangle; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None = None
        :param line_width: Width of the rectangle line; defaults to 0.
        :type line_width: int
        :param corner_radius: Radii of the corners of the rectangle; defaults to None.
        :type corner_radius: int | None
        :param border: Border of the rectangle; defaults to None.
        :type border: Border | None
        """
        self.top_left = top_left
        self.width = width
        self.height = height
        self.parent = parent
        self.children = []

        self.color = color
        self.line_width = line_width
        self.corner_radius = corner_radius
        self.border = border

        self._id = forge.core.utils.id.generate_random_id()

        if self.parent is not None:
            self.parent.children.append(self)

            if forge.hearth.settings.NON_CONSTRAINED_CHILDREN_USE_RELATIVE_POSITIONING:
                calculate_relative_positions(self.parent, [self.top_left])

    @property
    def center(self) -> forge.core.physics.vector.Vector2D:
        """
        Calculate the center of the rectangle.

        :return: Center of the rectangle.
        :rtype: forge.core.physics.vector.Vector2D
        """
        return forge.core.physics.vector.Vector2D(
            self.top_left.x + (self.width // 2),
            self.top_left.y + (self.height // 2)
        )

    @center.setter
    def center(self, value: forge.core.physics.vector.Vector2D) -> None:
        """
        Set the center of the rectangle and update the other vertices accordingly.

        :param value: New center of the rectangle.
        :type value: forge.core.physics.vector.Vector2D
        """
        self.top_left = forge.core.physics.vector.Vector2D(value.x - self.width // 2, value.y - self.height // 2)

    def id(self) -> int:
        """
        Get the unique ID of the rectangle.

        :return: ID of the rectangle.
        :rtype: int
        """
        return self._id

    def vertices(self, clockwise: bool = True) -> tuple[
        forge.core.physics.vector.Vector2D,
        forge.core.physics.vector.Vector2D,
        forge.core.physics.vector.Vector2D,
        forge.core.physics.vector.Vector2D
    ]:
        """
        Retrieve the vertices of the rectangle.

        :param clockwise: Whether to get the vertices in clockwise or counter-clockwise order; defaults to True.
        :type clockwise: bool
        :return: All the vertices of the rectangle.
        :rtype: tuple[
            forge.core.physics.vector.Vector2D, forge.core.physics.vector.Vector2D,
            forge.core.physics.vector.Vector2D, forge.core.physics.vector.Vector2D
        ]
        """
        top_left = copy.copy(self.top_left)
        top_right = forge.core.physics.vector.Vector2D(self.top_left.x + self.width, self.top_left.y)
        bottom_left = forge.core.physics.vector.Vector2D(self.top_left.x, self.top_left.y + self.height)
        bottom_right = forge.core.physics.vector.Vector2D(self.top_left.x + self.width, self.top_left.y + self.height)

        if clockwise:
            return top_left, top_right, bottom_right, bottom_left

        return top_left, bottom_left, bottom_right, top_right

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the rectangle to a renderer.

        :param renderer_name: Name of the renderer to which the rectangle is to be added; defaults to the base
                              UI renderer.
        :type renderer_name: str
        """
        forge.core.engine.renderer.get_renderer_from_name(renderer_name).elements.append(self)

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the rectangle to the display.

        :param display: Display to which the rectangle is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        pygame.draw.rect(
            display,
            self.color.as_pygame_color(), self.as_pygame_rect(),
            self.line_width, self.corner_radius if self.corner_radius is not None else -1
        )

        if self.border is not None:
            pygame.draw.rect(
                display,
                self.border.color.as_pygame_color(), self.as_pygame_rect(),
                self.border.width, self.border.radius if self.border.radius is not None else -1
            )

        if forge.hearth.settings.AUTO_RENDER_CHILDREN:
            for child in self.children:
                child.render(display)

    def update(self) -> None:
        """
        Update the rectangle.
        """
        if forge.hearth.settings.AUTO_UPDATE_CHILDREN:
            for child in self.children:
                child.update()

    def as_pygame_rect(self) -> pygame.rect.Rect:
        """
        Return the vertices the line as Pygame rect. Beneficial for internal interoperability with Pygame.

        :return: Pygame rect bounds of the rectangle.
        :rtype: pygame.rect.Rect
        """
        return pygame.rect.Rect(self.top_left.x, self.top_left.y, self.width, self.height)


class Circle(forge.hearth.elements.base.UIElement):
    """
    Basic circle in Hearth.
    """

    __slots__ = 'center', 'radius', 'parent', 'children', 'color', 'line_width', 'border', '_id'

    def __init__(
            self,
            center: forge.core.physics.vector.Vector2D, radius: int,
            color: forge.core.engine.color.Color,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: Border | None = None
    ) -> None:
        """
        Initialize the circle.

        :param center: Center of the circle.
        :type center: forge.core.physics.vector.Vector2D
        :param radius: Radius of the circle.
        :type radius: int
        :param color: Color of the center.
        :type color: forge.core.engine.color.Color
        :param parent: Parent of the circle; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the circle line; defaults to 0.
        :type line_width: int
        :param border: Border of the circle; defaults to None.
        :type border: Border | None
        """
        self.center = center
        self.radius = radius
        self.parent = parent
        self.children = []

        self.color = color
        self.line_width = line_width
        self.border = border

        self._id = forge.core.utils.id.generate_random_id()

        if self.parent is not None:
            self.parent.children.append(self)

    @property
    def top_left(self) -> forge.core.physics.vector.Vector2D:
        """
        Calculate the top left of the circle.

        :return: Top left of the circle.
        :rtype: forge.core.physics.vector.Vector2D
        """
        return self.center - forge.core.physics.vector.Vector2D(self.radius, self.radius)

    @top_left.setter
    def top_left(self, value: forge.core.physics.vector.Vector2D) -> None:
        """
        Set the top left of the circle and update the center accordingly.

        :param value: New top left of the circle.
        :type value: forge.core.physics.vector.Vector2D
        """
        self.center = value + forge.core.physics.vector.Vector2D(self.radius, self.radius)

    def id(self) -> int:
        """
        Get the unique ID of the circle.

        :return: ID of the circle.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the circle to a renderer.

        :param renderer_name: Name of the renderer to which the circle is to be added; defaults to the base
                              UI renderer.
        :type renderer_name: str
        """
        forge.core.engine.renderer.get_renderer_from_name(renderer_name).elements.append(self)

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the circle to the display.

        :param display: Display to which the circle is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        pygame.draw.circle(
            display,
            self.color.as_pygame_color(),
            self.center.as_tuple(), self.radius,
            self.line_width
        )

        if self.border is not None:
            pygame.draw.circle(
                display,
                self.border.color.as_pygame_color(),
                self.center.as_tuple(), self.radius,
                self.border.width
            )

        if forge.hearth.settings.AUTO_RENDER_CHILDREN:
            for child in self.children:
                child.render(display)

    def update(self) -> None:
        if forge.hearth.settings.AUTO_UPDATE_CHILDREN:
            for child in self.children:
                child.update()


class Polygon(forge.hearth.elements.base.UIElement):
    """
    Basic polygon in Hearth.
    """

    __slots__ = 'vertices', 'parent', 'children', 'color', 'parent', 'line_width', 'border', '_id'

    def __init__(
            self,
            vertices: list[forge.core.physics.vector.Vector2D],
            color: forge.core.engine.color.Color,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: Border | None = None
    ) -> None:
        """
        Initialize the polygon.

        :param vertices: Vertices of the polygon.
        :type vertices: list[forge.core.physics.vector.Vector2D]
        :param color: Color of the polygon.
        :type color: forge.core.engine.color.Color
        :param parent: Parent of the polygon; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the polygon line; defaults to 0.
        :type line_width: int
        :param border: Border of the circle; defaults to None.
        :type border: Border | None
        """
        self.vertices = vertices
        self.parent = parent
        self.children = []

        self.color = color
        self.line_width = line_width
        self.border = border

        self._id = forge.core.utils.id.generate_random_id()

        if self.parent is not None:
            self.parent.children.append(self)

    @property
    def top_left(self) -> forge.core.physics.vector.Vector2D:
        """
        Calculate the top left of the polygon.

        :return: Top left of the polygon.
        :rtype: forge.core.physics.vector.Vector2D
        """
        vertices = self.vertices

        return forge.core.physics.vector.Vector2D(
            min([vertex.x for vertex in vertices]),
            min([vertex.y for vertex in vertices])
        )

    @property
    def center(self) -> forge.core.physics.vector.Vector2D:
        """
        Calculate the center of the circle.

        :return: Center of the polygon.
        :rtype: forge.core.physics.vector.Vector2D
        """
        total = forge.core.physics.vector.zero()

        for vertex in self.vertices:
            total += vertex

        return total / len(self.vertices)

    def id(self) -> int:
        """
        Get the unique ID of the polygon.

        :return: ID of the polygon.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the polygon to a renderer.

        :param renderer_name: Name of the renderer to which the polygon is to be added; defaults to the base
                              UI renderer.
        :type renderer_name: str
        """
        forge.core.engine.renderer.get_renderer_from_name(renderer_name).elements.append(self)

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the polygon to the display.

        :param display: Display to which the polygon is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        pygame.draw.polygon(
            display,
            self.color.as_pygame_color(), self.as_tuples(),
            self.line_width
        )

        if self.border is not None:
            pygame.draw.polygon(
                display,
                self.border.color.as_pygame_color(), self.as_tuples(),
                self.border.width
            )

        if forge.hearth.settings.AUTO_RENDER_CHILDREN:
            for child in self.children:
                child.render(display)

    def update(self) -> None:
        """
        Update the polygon.
        """
        if forge.hearth.settings.AUTO_UPDATE_CHILDREN:
            for child in self.children:
                child.update()

    def as_tuples(self) -> list[tuple[float, float]]:
        """
        Return the vertices of the polygon as tuples. Beneficial for internal interoperability with Pygame.

        :return: Tuple of the vertices' x and y components respectively.
        :rtype: list[tuple[float, float]]
        """
        return [vertex.as_tuple() for vertex in self.vertices]

    def as_pygame_vectors(self) -> list[pygame.math.Vector2]:
        """
        Return the vertices of the polygon as Pygame vectors. Beneficial for internal interoperability with Pygame.

        :return: Tuple of the start and end points as Pygame vectors.
        :rtype: tuple[pygame.math.Vector2, pygame.math.Vector2]
        """
        return [vertex.as_pygame_vector() for vertex in self.vertices]


def calculate_relative_positions(
        parent: forge.hearth.elements.base.UIElement, vertices: list[forge.core.physics.vector.Vector2D]
) -> None:
    """
    Calculate the relative positions of children components given the parent's vertices.

    :param parent: Parent of the UI element.
    :type parent: forge.hearth.elements.base.UIElement
    :param vertices: List of vertices of the UI elements.
    :type vertices: list[forge.core.physics.vector.Vector2D]
    """
    parent_type = type(parent)

    if parent_type is Line:
        parent: Line

        for vertex in vertices:
            vertex += parent.start_point

    elif parent_type is Rectangle:
        parent: Rectangle

        for vertex in vertices:
            vertex += parent.top_left

    elif parent_type is Circle:
        parent: Circle

        for vertex in vertices:
            vertex += parent.center

    elif parent_type is Polygon:
        parent: Polygon
        top_left = parent.top_left

        for vertex in vertices:
            vertex += top_left

    else:
        raise ValueError(f'The UIElement {parent.__repr__()} cannot be a parent of other UIElements.')
