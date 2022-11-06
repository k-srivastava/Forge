"""
Basic text in Hearth.
"""
import dataclasses

import pygame

import forge.core.engine.color
import forge.core.engine.constants
import forge.core.engine.renderer
import forge.core.physics.vector
import forge.core.utils.aliases
import forge.core.utils.id
import forge.hearth.elements.base
import forge.hearth.elements.shapes
import forge.hearth.settings


class Text(forge.hearth.elements.base.UIElement):
    """
    Text class in Hearth.
    """

    __slots__ = 'text', 'font_size', 'top_left', 'font_face', 'background_color', 'anti_aliasing', '_render_font'

    def __init__(
            self,
            text: str, font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            top_left: forge.core.physics.vector.Vector2D = forge.core.physics.vector.zero(),
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            background_color: forge.core.engine.color.Color | None = None,
            parent: forge.hearth.elements.base.UIElement | None = None,
            anti_aliasing: bool = True
    ) -> None:
        """
        Initialize the text.

        :param text: Text to be rendered.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param top_left: Top-left vertex for the bounding box of the text.
        :type top_left: forge.core.physics.vector.Vector2D
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :type font_face: str
        :param color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type color: forge.core.engine.color.Color
        :param background_color: Color of the bounding box of the text; defaults to None.
        :type background_color: forge.core.engine.color.Color | None
        :param parent: Parent of the text; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        """
        self.text = text
        self.font_size = font_size
        self.top_left = top_left
        self.font_face = font_face
        self.anti_aliasing = anti_aliasing

        self.parent = parent
        self.children = []

        self.color = color
        self.background_color = background_color

        self._id = forge.core.utils.id.generate_random_id()
        self._render_font = self.as_pygame_font()

        if self.parent is not None:
            self.parent.children.append(self)

            if forge.hearth.settings.NON_CONSTRAINED_CHILDREN_USE_RELATIVE_POSITIONING:
                forge.hearth.elements.shapes.calculate_relative_positions(self.parent, [self.top_left])

    def __repr__(self) -> str:
        """
        Internal representation of the text.

        :return: Simple string with text data.
        :rtype: str
        """
        return f'Text -> Text: {self.text}, Font Size: {self.font_size}, Top Left: ({self.top_left.__repr__()}), ' \
               f'Child Count: {len(self.children)}'

    def __str__(self) -> str:
        """
        String representation of the text.

        :return: Detailed string with text information.
        :rtype: str
        """
        return f'Forge Text -> Text: {self.text}, Font Size: {self.font_size}, Font Face: {self.font_face}' \
               f'Top Left: ({self.top_left.__str__()}), Center: ({self.center.__str__()}), ' \
               f'Color: ({self.color.__str__()}), Background Color: ({self.background_color.__str__()}) ' \
               f'Parent: ({self.parent.__str__()}), Children: {self.children}'

    @property
    def center(self) -> forge.core.physics.vector.Vector2D:
        dimensions = self.dimensions()

        return forge.core.physics.vector.Vector2D(
            self.top_left.x + dimensions.x // 2,
            self.top_left.y + dimensions.y // 2
        )

    @center.setter
    def center(self, value: forge.core.physics.vector.Vector2D) -> None:
        dimensions = self.dimensions()

        self.top_left.x = value.x - dimensions.x // 2
        self.top_left.y = value.y - dimensions.y // 2

    def id(self) -> int:
        """
        Get the unique ID of the text.

        :return: ID of the text.
        :rtype: int
        """
        return self._id

    def dimensions(self) -> forge.core.physics.vector.Vector2D:
        """
        Calculate the width and height of the bounding box of the text.

        :return: Width and height of the bounding box of the text.
        :rtype: forge.core.physics.vector.Vector2D
        """
        return forge.core.physics.vector.from_tuple(self._render_font.size(self.text))

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER) -> None:
        """
        Add the text to a renderer.

        :param renderer_name: Name of the renderer to which the text is to be added; defaults to the base UI renderer.
        :type renderer_name: str
        """
        return forge.core.engine.renderer.get_renderer_from_name(renderer_name).elements.append(self)

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the text to the display.

        :param display: Display to which the text is to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        rendered_font: forge.core.utils.aliases.Surface = self._render_font.render(
            self.text, self.anti_aliasing,
            self.color.as_pygame_color(),
            self.background_color.as_pygame_color() if self.background_color is not None else None
        )
        font_rect = rendered_font.get_rect()

        font_rect.topleft = self.top_left.as_tuple()
        display.blit(rendered_font, font_rect)

    def update(self) -> None:
        """
        Update the text.
        """

    def as_pygame_font(self) -> pygame.font.Font:
        """
        Return the text font face and font size as a Pygame font. Beneficial for internal interoperability with Pygame.

        :return: Pygame font of the Hearth font.
        :rtype: pygame.font.Font
        """
        return pygame.font.Font(self.font_face, self.font_size)
