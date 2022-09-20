"""
Various base classes used throughout Hearth to define UI elements.
"""
from __future__ import annotations

import typing

import forge.core.engine.color
import forge.core.engine.constants
import forge.core.utils.aliases


class UIElement(typing.Protocol):
    """
    Base UI element class for Hearth.
    """
    parent: UIElement | None
    children: list[UIElement]
    color: forge.core.engine.color.Color
    _id: int

    def id(self) -> int:
        """
        Get the unique ID of the UI element.

        :return: ID of the UI element.
        :rtype: int
        """

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the UI element to a renderer.

        :param renderer_name: Name of the renderer to which the UI element is to be added; defaults to the base UI
                              renderer.
        :type renderer_name: str
        """

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the UI element to the display.

        :param display: Display to which the UI element is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """

    def update(self) -> None:
        """
        Update the UI element.
        """
