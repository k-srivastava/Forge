"""
Various base classes for Hearth components.
"""
import abc
import typing

import forge.core.engine.constants
import forge.core.utils.aliases
import forge.hearth.elements.base


class UIComponent(abc.ABC):
    """
    Base UI component class for Hearth.
    """
    children: list[forge.hearth.elements.base.UIElement | typing.Self]
    _id: int

    @abc.abstractmethod
    def id(self) -> int:
        """
        Get the unique ID of the UI component.

        :return: ID of the UI component.
        :rtype: int
        """

    @abc.abstractmethod
    def add_to_renderer(self) -> None:
        """
        Add the UI component and its base elements to their renderers respectively.
        """

    @abc.abstractmethod
    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the UI component and its elements to the display.

        :param display: Display to which the UI component and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """

    @abc.abstractmethod
    def update(self) -> None:
        """
        Update the UI component.
        """
