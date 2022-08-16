"""
Various base classes for Forge to organize code.
"""
import typing

import core.utils.aliases


class Renderable(typing.Protocol):
    """
    Base renderable class for Forge.
    """

    def render(self, display: core.utils.aliases.Surface) -> None:
        """
        Render the object to the display.

        :param display: Display to which the object is to be rendered.
        :type display: core.utils.aliases.Surface
        """
