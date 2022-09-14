"""
Various base classes for Hearth components.
"""
from __future__ import annotations

import typing

import forge.core.engine.constants
import forge.core.utils.aliases
import forge.hearth.elements.base


class UIComponent(typing.Protocol):
    """
    Base UI component class for Hearth.
    """
    children: list[forge.hearth.elements.base.UIElement | UIComponent]
    _id: int

    def id(self) -> int:
        """
        Get the unique ID of the UI component.

        :return: ID of the UI component.
        :rtype: int
        """

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        """
        Add the UI component and its base elements to their renderers respectively.

        :param component_renderer_name: Name of the renderer to which the UI component is to be added; defaults to the
                                        base component renderer.
        :type component_renderer_name: str
        :param ui_renderer_name: Name of the renderer to which the elements of the UI component are to be added;
                                 defaults to the base UI renderer.
        :type ui_renderer_name: str
        """

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the UI component and its elements to the display.

        :param display: Display to which the UI component and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """

    def update(self) -> None:
        """
        Update the UI component.
        """
