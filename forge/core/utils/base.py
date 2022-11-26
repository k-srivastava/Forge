"""
Various base classes for Forge to organize code.
"""
import abc

import forge.core.engine.constants
import forge.core.utils.aliases


class Renderable(abc.ABC):
    """
    Base renderable class for Forge.
    """

    @abc.abstractmethod
    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_OBJECT_RENDERER) -> None:
        """
        Add the object to a renderer.

        :param renderer_name: Name of the renderer to which the object is to be added; defaults to the base object
                              renderer.
        :type renderer_name: str
        """

    @abc.abstractmethod
    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the object to the display.

        :param display: Display to which the object is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
