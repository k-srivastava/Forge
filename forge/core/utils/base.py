"""
Various base classes for Forge to organize code.
"""
import abc

import forge.core.utils.aliases


class Renderable(abc.ABC):
    """
    Base renderable class for Forge.
    """

    @abc.abstractmethod
    def add_to_renderer(self) -> None:
        """
        Add the object to a renderer.
        """

    @abc.abstractmethod
    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the object to the display.

        :param display: Display to which the object is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
