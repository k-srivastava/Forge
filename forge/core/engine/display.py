"""
Base display for Forge.
"""
from __future__ import annotations

from typing import Optional

import pygame

from forge.core.engine.color import Color
from forge.core.engine.renderer import MasterRenderer
from forge.core.engine.sprite import Sprite
from forge.core.physics import vector
from forge.core.physics.vector import Vector2D
from forge.core.utils.aliases import Surface

# Store the current display in a list of length one.
# A list has to be used because a global variable becomes lengthy to implement.
_DISPLAY: list[Optional[Display]] = [None]


class Display:
    """
    Display class for Forge which is independent of its users.
    """

    __slots__ = (
        'title', 'max_fps', 'background_color', 'icon', 'object_renderer', 'ui_renderer', 'shape_renderer',
        'component_renderer', 'master_renderer', '_surface', '_clock', '_delta_time'
    )

    def __init__(
            self, width: int = 1280, height: int = 720, title: str = 'Forge', max_fps: int = 0,
            background_color: Color = Color(0, 0, 0),
            icon: Optional[Sprite] = None
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
        :type background_color: Color
        :param icon: Window icon sprite, if any; defaults to None.
        :type icon: Optional[Sprite]
        """
        if _DISPLAY[0] is not None:
            raise SyntaxError()

        self.title = title
        self.max_fps = max_fps
        self.background_color = background_color
        self.icon = icon

        self.master_renderer = MasterRenderer()

        self._surface = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._delta_time: float = 0

        pygame.display.set_caption(title)

        if icon is not None:
            pygame.display.set_icon(icon.surface)

        _DISPLAY[0] = self

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
    def size() -> Vector2D:
        """
        Get the size of the display as a Forge Vector2D.

        :return: Size of the display.
        :rtype: forge.core.physics.vector.Vector2D
        """
        return vector.from_tuple(pygame.display.get_window_size())

    def surface(self) -> Surface:
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

        # self.object_renderer.render(self._surface)
        # self.ui_renderer.render(self._surface)
        # self.shape_renderer(self._surface)
        # self.component_renderer.render(self._surface)
        self.master_renderer.render(self._surface)

    def update(self) -> None:
        """
        Update the display and all the display renderers. Also calculate the delta time after each update loop.
        """
        self._delta_time = self._clock.tick(self.max_fps) / 1000

        # self.object_renderer.update(self._delta_time)
        # self.ui_renderer.update(self._delta_time)
        # self.shape_renderer.update(self._delta_time)
        # self.component_renderer.update(self._delta_time)
        self.master_renderer.update(self._delta_time)

        pygame.display.flip()


def get_display() -> Optional[Display]:
    """
    Retrieve the current display.

    :return: Current display; if it exists.
    :rtype: Optional[Display]
    """
    return _DISPLAY[0]
