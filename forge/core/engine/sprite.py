"""
Sprites in Forge.
"""
from dataclasses import dataclass, field

import pygame

from forge.core.physics.vector import Vector2D
from forge.core.utils.aliases import Surface


@dataclass(slots=True)
class Sprite:
    """
    Forge's representation of a generic sprite, without positional data.
    """
    filename: str
    _scale: float = field(default=1.0)
    surface: Surface = field(init=False)
    _surface_raw: Surface = field(init=False)

    def __post_init__(self) -> None:
        self._surface_raw = pygame.image.load(self.filename).convert_alpha()
        self.surface = pygame.transform.smoothscale_by(self._surface_raw, self._scale)

    @property
    def scale(self) -> float:
        """
        Getter for the scale of the sprite.

        :return: Scale of the sprite.
        :rtype: float
        """
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        """
        Setter for the scale of the sprite. Also updates the sprite's surface.

        :param value: New value for the scale.
        :type value: float
        """
        self._scale = value
        self.surface = pygame.transform.smoothscale_by(self._surface_raw, self._scale)

    def width(self, with_scale: bool = True) -> int:
        """
        Width of the sprite.

        :param with_scale: Whether to include the scaling factor when calculating the width; defaults to True.
        :type with_scale: bool

        :return: Width of the sprite.
        :rtype: int
        """
        return pygame.image.load(self.filename).convert_alpha().get_width() if with_scale else self.surface.get_width()

    def height(self, with_scale: bool = True) -> int:
        """
        Height of the sprite.

        :param with_scale: Whether to include the scaling factor when calculating the height; defaults to True.
        :type with_scale: bool

        :return: Height of the sprite.
        :rtype: int
        """
        return pygame.image.load(self.filename).convert_alpha().get_height() if with_scale else self.surface.get_width()

    def render(self, display: Surface, position: Vector2D) -> None:
        """
        Render the sprite as a Pygame surface to the display at its given position.

        :param display: Display to which the sprite is to be rendered.
        :type display: Surface
        :param position: Position at which the sprite is to be rendered.
        :type position: Vector2D
        """
        display.blit(self.surface, position.as_tuple())
