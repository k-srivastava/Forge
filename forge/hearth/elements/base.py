"""Various base classes used throughout Hearth to define shapes and UI elements."""
from __future__ import annotations

from abc import abstractmethod
from copy import copy
from typing import Optional, Self, TYPE_CHECKING

from forge.core.engine import renderer
from forge.core.engine.color import Color
from forge.core.physics.vector import Vector2D
from forge.core.physics.world import MAX_BODY_AREA, MIN_BODY_AREA
from forge.core.utils import id
from forge.core.utils.aliases import Surface
from forge.core.utils.base import Renderable
from forge.core.utils.exceptions import BodyAreaError
from forge.hearth.elements.border import Border

if TYPE_CHECKING:
    from forge.hearth.components.base import UIComponent


class Shape(Renderable):
    """Shape base class for Hearth."""
    __slots__ = 'color', 'line_width', 'border', 'parent', 'children', '_id', '_previous_position'

    def __init__(
            self, color: Color, line_width: int = 0, border: Optional[Border] = None,
            parent: Optional[UIComponent | UIElement | Shape] = None
    ) -> None:
        """
        Initialize the shape.

        :param color: Color of the shape.
        :type color: Color
        :param border: Border of the shape; defaults to None.
        :type border: Optional[Border]
        :param parent: Parent of the shape; defaults to None.
        :type parent: Optional[UIElement | Shape]

        :raises BodyAreaError: Size of the shape should be within the given body size constraints, if being checked.
        """
        self.color = color
        self.line_width = line_width
        self.border = border
        self.parent = parent
        self.children: list[Shape] = []

        self._id = id.generate_random_id()
        self._previous_position = copy(self.top_left)

        if self.parent is not None:
            self.top_left += self.parent.top_left
            self.parent.children.append(self)

        if not MIN_BODY_AREA <= self.area <= MAX_BODY_AREA:
            raise BodyAreaError(self.area, MIN_BODY_AREA, MAX_BODY_AREA)

    def id(self) -> int:
        """
        Get the unique ID of the shape.

        :return: ID of the shape.
        :rtype: int
        """
        return self._id

    @property
    @abstractmethod
    def top_left(self) -> Vector2D:
        """
        Getter for the top-left-most point of the shape.

        :return: Top-left-most point of the shape.
        :rtype: Vector2D
        """

    @top_left.setter
    @abstractmethod
    def top_left(self, value: Vector2D) -> None:
        """
        Setter for the top-left-most point of the shape.

        :param value: New value of the top-left-most point of the shape.
        :type value: Vector2D
        """

    @property
    @abstractmethod
    def center(self) -> Vector2D:
        """
        Getter for the center point of the shape.

        :return: Center point of the shape.
        :rtype: Vector2D
        """

    @center.setter
    @abstractmethod
    def center(self, value: Vector2D) -> None:
        """
        Setter for the center point of the shape.

        :param value: New value of the center of the shape.
        :type value: Vector2D
        """

    @property
    @abstractmethod
    def area(self) -> float:
        """
        Getter for the area of the shape.

        :return: Area of the shape.
        :rtype: float
        """

    @property
    @abstractmethod
    def perimeter(self) -> float:
        """
        Getter for the perimeter of the shape.

        :return: Perimeter of the shape.
        :rtype: float
        """

    @abstractmethod
    def computed_width(self) -> float:
        ...

    @abstractmethod
    def computed_height(self) -> float:
        ...

    def add_to_renderer(self) -> None:
        """Add the shape to a renderer."""
        renderer.get_master_renderer().add_shape(self)

    def render(self, display: Surface) -> None:
        """
        Render the shape to the display.

        :param display: Display to which the shape is to be rendered.
        :type display: Surface
        """
        for child in self.children:
            child.render(display)

    def update(self) -> None:
        """Update the shape."""
        if self.top_left != self._previous_position:
            displacement: Vector2D = self.top_left - self._previous_position

            for child in self.children:
                child.top_left += displacement

            self._previous_position = copy(self.top_left)

        for child in self.children:
            child.update()


class UIElement(Renderable):
    """UI element abstract base class for Hearth."""
    __slots__ = 'color', 'parent', 'children', '_id', '_previous_position'

    def __init__(self, color: Color, parent: Optional[UIComponent | Self] = None) -> None:
        """
        Initialize the UI element.

        :param color: Color of the UI element.
        :type color: Color
        :param parent: Parent of the UI element; defaults to None.
        :type parent: Optional[Self]
        """
        self.color = color
        self.parent = parent
        self.children: list[Self | Shape] = []

        self._id = id.generate_random_id()
        self._previous_position = self.top_left

        if self.parent is not None:
            self.parent.children.append(self)

    def id(self) -> int:
        """
        Get the unique ID of the UI element.

        :return: ID of the UI element.
        :rtype: int
        """
        return self._id

    @property
    @abstractmethod
    def top_left(self) -> Vector2D:
        """
        Getter for the top-left-most point of the shape.

        :return: Top-left-most point of the shape.
        :rtype: Vector2D
        """

    @top_left.setter
    @abstractmethod
    def top_left(self, value: Vector2D) -> None:
        """
        Setter for the top-left-most point of the shape.

        :param value: New value of the top-left-most point of the shape.
        :type value: Vector2D
        """

    @property
    @abstractmethod
    def center(self) -> Vector2D:
        """
        Getter for the center point of the shape.

        :return: Center point of the shape.
        :rtype: Vector2D
        """

    @center.setter
    @abstractmethod
    def center(self, value: Vector2D) -> None:
        """
        Setter for the center point of the shape.

        :param value: New value of the center of the shape.
        :type value: Vector2D
        """

    def add_to_renderer(self) -> None:
        """Add the UI element to a renderer."""
        renderer.get_master_renderer().add_element(self)

    def render(self, display: Surface) -> None:
        """
        Render the UI element to the display.

        :param display: Display to which the UI element is to be rendered.
        :type display: Surface
        """
        for child in self.children:
            child.render(display)

    def update(self) -> None:
        """Update the UI element."""
        if self.top_left != self._previous_position:
            displacement: Vector2D = self.top_left - self._previous_position

            for child in self.children:
                child.top_left += displacement

            self._previous_position = self.top_left

        for child in self.children:
            child.update()
