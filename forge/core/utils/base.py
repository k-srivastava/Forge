"""
Various base classes for Forge to organize code.
"""
from abc import ABC, abstractmethod

from forge.core.utils.aliases import Surface


class Renderable(ABC):
    """
    Base renderable class for Forge.
    """

    @abstractmethod
    def add_to_renderer(self) -> None:
        """
        Add the object to a renderer.
        """

    @abstractmethod
    def render(self, display: Surface) -> None:
        """
        Render the object to the display.

        :param display: Display to which the object is to be rendered.
        :type display: Surface
        """
