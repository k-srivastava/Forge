"""Various base classes used throughout Hearth to define more complex UI elements."""
from forge.core.engine import renderer
from forge.core.utils import id
from forge.core.utils.aliases import Surface
from forge.core.utils.base import Renderable
from forge.hearth.elements.base import Shape, UIElement


class UIComponent(Renderable):
    """UI component base class for Hearth."""
    __slots__ = 'children', '_id'

    def __init__(self, children: list[UIElement | Shape]) -> None:
        self.children = children
        self._id = id.generate_random_id()

        for child in self.children:
            child.parent = self

    def id(self) -> int:
        """
        Get the unique ID of the UI component.

        :return: ID of the UI component.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self) -> None:
        """Add the UI component to a renderer."""
        renderer.get_master_renderer().add_component(self)

    def render(self, display: Surface) -> None:
        """
        Render the UI component to the display.

        :param display: Display to which the UI component is to be rendered.
        :type display: Surface
        """
        for child in self.children:
            child.render(display)

    def update(self) -> None:
        """Update the UI component."""
        for child in self.children:
            child.update()
