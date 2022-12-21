"""
Various base classes used throughout Hearth to define UI elements.
"""
import abc
import dataclasses
import typing

import forge.core.engine.color
import forge.core.engine.constants
import forge.core.physics.vector
import forge.core.utils.aliases


@dataclasses.dataclass(slots=True)
class Border:
    """
    Border for each supported shape in Hearth.
    """

    width: int
    color: forge.core.engine.color.Color
    radius: int | None = None  # A border radius is only applicable for rectangles.

    def __repr__(self) -> str:
        """
        Internal representation of the border.

        :return: Simple string with border data.
        :rtype: str
        """
        return f'Border -> Width: {self.width}, Radius: {self.radius}, Color: ({self.color.__repr__()})'

    def __str__(self) -> str:
        """
        String representation of the border.

        :return: Detailed string with border data.
        :rtype: str
        """
        return f'Forge Border -> Width: {self.width}, Radius: {self.radius}, Color: ({self.color.__repr__()})'


class Shape(abc.ABC):
    color: forge.core.engine.color.Color
    border: Border | None
    parent: forge.hearth.elements.base.UIElement | None
    _id: int

    @abc.abstractmethod
    def id(self) -> int:
        """"""

    @property
    @abc.abstractmethod
    def top_left(self) -> forge.core.physics.vector.Vector2D:
        """"""

    @top_left.setter
    @abc.abstractmethod
    def top_left(self, value: forge.core.physics.vector.Vector2D) -> None:
        """"""

    @property
    @abc.abstractmethod
    def center(self) -> forge.core.physics.vector.Vector2D:
        """"""

    @center.setter
    @abc.abstractmethod
    def center(self, value: forge.core.physics.vector.Vector2D) -> None:
        """"""

    @abc.abstractmethod
    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_SHAPE_RENDERER) -> None:
        """"""

    @abc.abstractmethod
    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """"""

    @abc.abstractmethod
    def update(self) -> None:
        """"""


class UIElement(abc.ABC):
    """
    Base UI element class for Hearth.
    """
    parent: typing.Self | None
    children: list[typing.Self | Shape]
    color: forge.core.engine.color.Color
    _id: int

    @abc.abstractmethod
    def id(self) -> int:
        """
        Get the unique ID of the UI element.

        :return: ID of the UI element.
        :rtype: int
        """

    @abc.abstractmethod
    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the UI element to a renderer.

        :param renderer_name: Name of the renderer to which the UI element is to be added; defaults to the base UI
                              renderer.
        :type renderer_name: str
        """

    @abc.abstractmethod
    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the UI element to the display.

        :param display: Display to which the UI element is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """

    @abc.abstractmethod
    def update(self) -> None:
        """
        Update the UI element.
        """
