"""
Base display for Forge.
"""
from __future__ import annotations

import pygame

import forge.core.engine.color
import forge.core.engine.constants
import forge.core.engine.renderer
import forge.core.engine.sprite
import forge.core.physics.vector
import forge.core.utils.aliases

# Store the current display in a list of length one.
# A list has to be used because a global variable becomes lengthy to implement.
_DISPLAY: list[Display | None] = [None]


class Display:
    """
    Display class for Forge which is independent of its users.
    """

    __slots__ = (
        'title', 'max_fps', 'background_color', 'icon', 'object_renderer', 'ui_renderer', 'shape_renderer',
        'component_renderer', '_surface', '_clock', '_delta_time'
    )

    def __init__(
            self, width: int = 1280, height: int = 720, title: str = 'Forge', max_fps: int = 0,
            background_color: forge.core.engine.color.Color = forge.core.engine.color.Color(0, 0, 0),
            icon: forge.core.engine.sprite.Sprite | None = None
    ) -> None:
        """
        Initialize the Forge display.

        :param width: Width of the display; defaults to 1280.
        :type width: int
        :param height: Height of the display; defaults to 720.
        :type height: int
        :param title: Title of the display; defaults to 'Forge'.
        :param max_fps: Maximum FPS of the display; defaults to 0.
        :type max_fps: int
        :param background_color: Background color of the display; defaults to black.
        :type background_color: forge.core.engine.color.Color
        :param icon: Window icon sprite, if any; defaults to None.
        :type icon: forge.core.engine.sprite.Sprite | None
        """
        if _DISPLAY[0] is not None:
            raise SyntaxError()

        self.title = title
        self.max_fps = max_fps
        self.background_color = background_color
        self.icon = icon

        self.object_renderer = forge.core.engine.renderer.ObjectRenderer(
            forge.core.engine.constants.DISPLAY_OBJECT_RENDERER
        )

        self.ui_renderer = forge.core.engine.renderer.UIRenderer(
            forge.core.engine.constants.DISPLAY_UI_RENDERER
        )

        self.component_renderer = forge.core.engine.renderer.ComponentRenderer(
            forge.core.engine.constants.DISPLAY_SHAPE_RENDERER
        )

        self.component_renderer = forge.core.engine.renderer.ComponentRenderer(
            forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER
        )

        self._surface = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._delta_time: float = 0

        pygame.display.set_caption(title)

        if icon is not None:
            pygame.display.set_icon(icon.as_pygame_surface())

        _DISPLAY[0] = self

    def __repr__(self) -> str:
        """
        Internal representation of the display.

        :return: Simple string with basic display data.
        :rtype: str
        """
        return f'Display -> Width: {self.width()}, Height: {self.height()}, Title: {self.title}'

    def __str__(self) -> str:
        """
        String representation of the display.

        :return: Detailed string with display data.
        :rtype: str
        """
        return f'Forge Display -> Width: {self.width()}, Height: {self.height()}, Title: {self.title}, ' \
               f'Max FPS: {self.max_fps}, Icon: ({self.icon.__str__()})'

    @staticmethod
    def width() -> int:
        """
        Get the width of the display.

        :return: Width of the display.
        :rtype: int
        """
        return pygame.display.get_window_size()[0]

    @staticmethod
    def height() -> int:
        """
        Get the height of the display.

        :return: Height of the display.
        :rtype: int
        """
        return pygame.display.get_window_size()[1]

    @staticmethod
    def size() -> forge.core.physics.vector.Vector2D:
        """
        Get the size of the display as a Forge Vector2D.

        :return: Size of the display.
        :rtype: forge.core.physics.vector.Vector2D
        """
        return forge.core.physics.vector.from_tuple(pygame.display.get_window_size())

    def surface(self) -> forge.core.utils.aliases.Surface:
        """
        Get the surface of the display.

        :return: Surface of the display.
        :rtype: forge.core.utils.aliases.Surface
        """
        return self._surface

    def render(self) -> None:
        """
        Render the display background color and call all the display renderers to render from their pools.
        """
        self._surface.fill(self.background_color.as_tuple())

        self.object_renderer.render(self._surface)
        self.ui_renderer.render(self._surface)
        self.shape_renderer(self._surface)
        self.component_renderer.render(self._surface)

    def update(self) -> None:
        """
        Update the display and all the display renderers. Also calculate the delta time after each update loop.
        """
        self._delta_time = self._clock.tick(self.max_fps) / 1000

        self.object_renderer.update(self._delta_time)
        self.ui_renderer.update(self._delta_time)
        self.shape_renderer.update(self._delta_time)
        self.component_renderer.update(self._delta_time)

        pygame.display.flip()


def get_display() -> Display | None:
    """
    Retrieve the current display.

    :return: Current display; if it exists.
    :rtype: Display | None
    """
    return _DISPLAY[0]
