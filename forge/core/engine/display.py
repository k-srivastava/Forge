"""
Base display for Forge.
"""
import pygame

import forge.core.engine.color
import forge.core.engine.constants
import forge.core.engine.renderer
import forge.core.physics.vector


class Display:
    """
    Display class for Forge which is independent of its users.
    """

    __slots__ = 'title', 'max_fps', 'background_color', 'object_renderer', '_surface', '_clock', '_delta_time'

    def __init__(
            self, width: int, height: int, title: str, max_fps: int = 0,
            background_color: forge.core.engine.color.Color = forge.core.engine.color.Color(0, 0, 0)
    ) -> None:
        """
        Initialise the Forge display.

        :param width: Width of the display.
        :type width: int
        :param height: Height of the display.
        :type height: int
        :param title: Title of the display.
        :param max_fps: Maximum FPS of the display; defaults to 0.
        :type max_fps: int
        :param background_color: Background color of the display.
        :type background_color: forge.core.engine.color.Color
        """
        self.title = title
        self.max_fps = max_fps
        self.background_color = background_color

        self.object_renderer = forge.core.engine.renderer.ObjectRenderer(
            forge.core.engine.constants.DISPLAY_OBJECT_RENDERER, [], [], [], []
        )

        # Private variables.
        self._surface = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()
        self._delta_time: float = 0

        pygame.display.set_caption(title)

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

    def render(self) -> None:
        """
        Render the display background color and call all the display renderers to render from their pools.
        """
        self._surface.fill(self.background_color.as_tuple())
        self.object_renderer.render(self._surface)

    def update(self) -> None:
        """
        Update the display and all the display renderers. Also calculate the delta time after each update loop.
        """
        self._delta_time = self._clock.tick(self.max_fps) / 1000
        self.object_renderer.update(self._delta_time)

        pygame.display.flip()
