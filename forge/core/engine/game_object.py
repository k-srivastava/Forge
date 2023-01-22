"""
Game objects in Forge.
"""
import dataclasses

import forge.core.engine.renderer
import forge.core.engine.sprite
import forge.core.managers.keyboard
import forge.core.physics.vector
import forge.core.utils.aliases
import forge.core.utils.base
import forge.core.utils.id
import forge.hearth.elements.base

_GAME_OBJECTS: dict[int, 'GameObject'] = {}


class GameObject(forge.core.utils.base.Renderable):
    """
    Forge's representation of a game object.
    """
    __slots__ = ('name', 'position', 'shape', 'sprite', 'sprite_offset', '_id')

    def __init__(
            self,
            name: str, position: forge.core.physics.vector.Vector2D,
            shape: forge.hearth.elements.base.Shape | None = None,
            sprite: forge.core.engine.sprite.Sprite | None = None,
            sprite_offset: forge.core.physics.vector.Vector2D = forge.core.physics.vector.zero()
    ) -> None:
        """
        Initialize the game object.

        :param name: Name of the game object.
        :type name: str
        :param position: Position of the game object.
        :type position: forge.core.physics.vector.Vector2D
        :param shape: Shape of the game object; defaults to None.
        :type shape: forge.hearth.elements.base.Shape | None
        :param sprite: Sprite of the game object; defaults to None.
        :type sprite: forge.core.engine.sprite.Sprite | None
        :param sprite_offset: Offset position of the sprite; defaults to a zero vector.
        :type sprite_offset: forge.core.physics.vector.Vector2D
        """
        self.name = name
        self.position = position
        self.shape = shape
        self.sprite = sprite
        self.sprite_offset = sprite_offset
        self._id = forge.core.utils.id.generate_random_id()

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
        forge.core.engine.renderer.get_master_renderer().add_game_object(self)

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
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
