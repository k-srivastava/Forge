"""
Debug shape drawing in Forge without using the render pipeline.
"""
import pygame

import forge.core.engine.color
import forge.core.engine.display
import forge.core.physics.vector
import forge.hearth.elements.shapes


def draw_line(
        start: forge.core.physics.vector.Vector2D, end: forge.core.physics.vector.Vector2D,
        color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
        width: int = 3
) -> None:
    """
    Draw a line onto the display directly.

    :param start: Start point of the line.
    :type start: forge.core.physics.vector.Vector2D
    :param end: End point of the line.
    :type end: forge.core.physics.vector.Vector2D
    :param color: Color of the line; defaults to (R: 255, G: 255, B: 255) - white.
    :type color: forge.core.engine.color.Color
    :param width: Width of the line; defaults to 3.
    :type width: int
    """
    pygame.draw.line(
        forge.core.engine.display.get_display().surface(), color.as_pygame_color(), start.as_tuple(), end.as_tuple(),
        width
    )


def draw_rectangle(
        top_left: forge.core.physics.vector.Vector2D,
        width: int, height: int,
        color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 80, 80),
        line_width: int = 0
) -> None:
    """
    Draw a rectangle onto the display directly.

    :param top_left: Top-left position of the rectangle.
    :type top_left: forge.core.physics.vector.Vector2D
    :param width: Width of the rectangle.
    :type width: int
    :param height: Height of the rectangle.
    :type height: int
    :param color: Color of the rectangle; defaults to (R: 255, G: 80, B: 80) - light red.
    :type color: forge.core.engine.color.Color
    :param line_width: Width of the line of the rectangle; defaults to 0.
    :type line_width: int
    """
    pygame.draw.rect(
        forge.core.engine.display.get_display().surface(), color.as_pygame_color(),
        pygame.rect.Rect(top_left.x, top_left.y, width, height), line_width
    )


def draw_circle(
        center: forge.core.physics.vector.Vector2D, radius: int = 10,
        color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 80, 80)
) -> None:
    """
    Draw a debug circle onto the display directly.

    :param center: Center of the circle.
    :type center: forge.core.physics.vector.Vector2D
    :param radius: Radius of the circle; defaults to 10.
    :type radius: int
    :param color: Color of the circle; defaults to (R: 255, G: 80, B: 80) - light red.
    :type color: forge.core.engine.color.Color
    """
    pygame.draw.circle(
        forge.core.engine.display.get_display().surface(), color.as_pygame_color(), center.as_tuple(), radius
    )


def draw_polygon(
        vertices: list[forge.core.physics.vector.Vector2D],
        color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 80, 80),
        line_width: int = 0
) -> None:
    """
    Draw a polygon onto the display directly.

    :param vertices: List of vertices of the polygon.
    :type vertices: list[forge.core.physics.vector.Vector2D]
    :param color: Color of the polygon; defaults to (R: 255, G: 80, B: 80) - light red.
    :type color: forge.core.engine.color.Color
    :param line_width: Width of the line of the polygon; defaults to 0.
    :type line_width: int
    """
    pygame.draw.polygon(
        forge.core.engine.display.get_display().surface(), color.as_pygame_color(),
        [vertex.as_tuple() for vertex in vertices], line_width
    )
