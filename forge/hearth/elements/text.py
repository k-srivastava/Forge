"""Basic text in Hearth."""
from typing import Optional

import pygame

from forge.core.engine.color import Color
from forge.core.physics.vector import Vector2D
from forge.core.utils.aliases import Surface
from forge.hearth.elements.base import UIElement
from forge.hearth.settings import DEFAULT_FONT_FACE, DEFAULT_FONT_SIZE


class Text(UIElement):
    """Text class in Hearth."""
    __slots__ = 'text', 'font_size', 'font_face', 'background_color', 'anti_aliasing', '_top_left', '_render_font'

    def __init__(self, text: str, top_left: Vector2D, font_size: int = DEFAULT_FONT_SIZE,
                 font_face: str = DEFAULT_FONT_FACE, color: Color = Color(255, 255, 255),
                 background_color: Optional[Color] = None, parent: Optional[UIElement] = None,
                 anti_aliasing: bool = True) -> None:
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.background_color = background_color
        self.anti_aliasing = anti_aliasing

        self._top_left = top_left
        self._render_font = self.as_pygame_font()

        super().__init__(color, parent)

    @property
    def top_left(self) -> Vector2D:
        """
        Getter for the top-left of the text box.

        :return: Top-left of the text box.
        :rtype: Vector2D
        """
        return self._top_left

    @top_left.setter
    def top_left(self, value: Vector2D) -> None:
        """
        Setter for the top-left of the text box.

        :param value: New top-left of the text box.
        :type value: Vector2D
        """
        self._top_left = value

    @property
    def center(self) -> Vector2D:
        """
        Getter for the center of the text box.

        :return: Center of the text box.
        :rtype: Vector2D
        """
        return Vector2D(self._top_left.x + self.width // 2, self._top_left.y + self.height // 2)

    @center.setter
    def center(self, value: Vector2D) -> None:
        """
        Setter for the center of the text box.

        :param value: New center of the text box.
        :type value: Vector2D
        """
        self._top_left.x = value.x - self.width // 2
        self._top_left.y = value.y - self.height // 2

    @property
    def width(self) -> int:
        """
        Width of the text box.

        :return: Width of the text box.
        :rtype: int
        """
        return self._render_font.size(self.text)[0]

    @property
    def height(self) -> int:
        """
        Height of the text box.

        :return: Height of the text box.
        :rtype: int
        """
        return self._render_font.size(self.text)[1]

    def render(self, display: Surface) -> None:
        """
        Render the text to the display.

        :param display: Display to which the text is to be rendered.
        :type display: Surface
        """
        rendered_font: Surface = self._render_font.render(
            self.text, self.anti_aliasing, self.color.as_tuple(),
            self.background_color.as_tuple() if self.background_color is not None else None
        )
        font_rect = rendered_font.get_rect()

        font_rect.topleft = self._top_left.as_tuple()
        display.blit(rendered_font, font_rect)

    def as_pygame_font(self) -> pygame.font.Font:
        """
        Return the text font face and font size as a Pygame font. Beneficial for internal interoperability with Pygame.

        :return: Pygame font of the Hearth font.
        :rtype: pygame.font.Font
        """
        return pygame.font.Font(self.font_face, self.font_size)
