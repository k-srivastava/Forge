"""
Sprites in Forge.
"""
import dataclasses

import pygame

import forge.core.physics.vector
import forge.core.utils.aliases


@dataclasses.dataclass(slots=True)
class Sprite:
    """
    Forge's representation of a generic sprite, without positional data.
    """
    filename: str

    def __repr__(self) -> str:
        """
        Internal representation of the sprite.

        :return: Simple string with sprite data.
        :rtype: str
        """
        return f'Sprite -> Filename: {self.filename}'

    def __str__(self) -> str:
        """
        String representation of the sprite.

        :return: Detailed string with sprite data.
        :rtype: str
        """
        return f'Forge Sprite -> Filename: {self.filename}'

    def render(self, display: forge.core.utils.aliases.Surface, position: forge.core.physics.vector.Vector2D) -> None:
        """
        Render the sprite as a Pygame surface to the display at its given position.

        :param display: Display to which the sprite is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        :param position: Position at which the sprite is to be rendered.
        :type position: forge.core.physics.vector.Vector2D
        """
        display.blit(self.as_pygame_surface(), position.as_tuple())

    def as_pygame_surface(self) -> pygame.surface.Surface:
        """
        Return the sprite as a Pygame surface. Beneficial for internal interoperability with Pygame.

        :return: Pygame surface containing the image data.
        :rtype: pygame.surface.Surface
        """
        return pygame.image.load(self.filename).convert_alpha()
