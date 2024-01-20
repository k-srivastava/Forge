"""
Game objects in Forge.
"""
from typing import Optional

from forge.core.engine import renderer
from forge.core.engine.sprite import Sprite
from forge.core.physics.vector import Vector2D
from forge.core.utils import id
from forge.core.utils.aliases import Surface
from forge.core.utils.base import Renderable
from forge.hearth.elements.base import Shape

_GAME_OBJECTS: dict[int, 'GameObject'] = {}


class GameObject(Renderable):
    """
    Forge's representation of a game object.
    """
    __slots__ = ('name', 'position', 'shape', 'sprite', 'sprite_offset', '_id')

    def __init__(
            self,
            name: str, position: Vector2D,
            shape: Optional[Shape] = None,
            sprite: Optional[Sprite] = None,
            sprite_offset: Vector2D = Vector2D.zero()
    ) -> None:
        """
        Initialize the game object.

        :param name: Name of the game object.
        :type name: str
        :param position: Position of the game object.
        :type position: Vector2D
        :param shape: Shape of the game object; defaults to None.
        :type shape: Optional[Shape]
        :param sprite: Sprite of the game object; defaults to None.
        :type sprite: Optional[Sprite]
        :param sprite_offset: Offset position of the sprite; defaults to a zero vector.
        :type sprite_offset: Vector2D
        """
        self.name = name
        self.position = position
        self.shape = shape
        self.sprite = sprite
        self.sprite_offset = sprite_offset
        self._id = id.generate_random_id()

        _GAME_OBJECTS[self._id] = self

    def id(self) -> int:
        """
        Get the unique ID of the game object.

        :return: ID of the game object.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self) -> None:
        """
        Add the game object to the renderer.
        """
        renderer.get_master_renderer().add_game_object(self)

    def render(self, display: Surface) -> None:
        """
        Render the game object to the display.

        :param display: Display to which the game object is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        if self.shape is not None:
            self.shape.render(display)

        if self.sprite is not None:
            self.sprite.render(display, self.position + self.sprite_offset)

    def update(self, delta_time: float) -> None:
        """
        Update the game object.

        :param delta_time: Delta time for the current pass.
        :type delta_time: float
        """
