"""Debug shape drawing in Hearth without using the Hearth render pipeline."""
from math import pi

import pygame

from forge.core.engine import display
from forge.core.engine.color import Color
from forge.core.physics.vector import Vector2D
from forge.core.physics.world import MAX_BODY_AREA, MIN_BODY_AREA
from forge.core.utils import exceptions
from forge.core.utils.exceptions import BodyAreaError


def draw_line(start: Vector2D, end: Vector2D, color: Color = Color(255, 255, 255), width: int = 3) -> None:
    """
    Draw a line onto the display directly.

    :param start: Start point of the line.
    :type start: Vector2D
    :param end: End point of the line.
    :type end: Vector2D
    :param color: Color of the line; defaults to (R: 255, G: 255, B: 255) - white.
    :type color: Color
    :param width: Width of the line; defaults to 3.
    :type width: int
    """
    pygame.draw.line(display.get_display().surface(), color.as_tuple(), start.as_tuple(), end.as_tuple(), width)


def draw_rectangle(top_left: Vector2D, width: int, height: int, color: Color = Color(255, 80, 80), line_width: int = 0,
                   check_for_area_bounds: bool = False) -> None:
    """
    Draw a rectangle onto the display directly.

    :param top_left: Top-left position of the rectangle.
    :type top_left: Vector2D
    :param width: Width of the rectangle.
    :type width: int
    :param height: Height of the rectangle.
    :type height: int
    :param color: Color of the rectangle; defaults to (R: 255, G: 80, B: 80) - dark red.
    :type color: Color
    :param line_width: Width of the line of the rectangle; defaults to 0 - solid rectangle.
    :type line_width: int
    :param check_for_area_bounds: Whether to check if the area of the rectangle lies within the given constraints;
                                  defaults to False.
    :type check_for_area_bounds: bool

    :raises BodyAreaError: Size of the rectangle should be within the given body size constraints, if being checked.
    """
    if check_for_area_bounds:
        area: int = width * height

        if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
            raise BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    pygame.draw.rect(
        display.get_display().surface(), color.as_tuple(), pygame.rect.Rect(top_left.x, top_left.y, width, height),
        line_width
    )


def draw_circle(center: Vector2D, radius: int, color: Color = Color(255, 80, 80), line_width: int = 0,
                check_for_area_bounds: bool = False) -> None:
    """
    Draw a circle onto the display directly.

    :param center: Center position of the rectangle.
    :type center: Vector2D
    :param radius: Radius of the circle.
    :type radius: int
    :param color: Color of the circle; defaults to (R: 255, G: 80, B: 80) - dark red.
    :type color: Color
    :param line_width: Width of the line of the circle; defaults to 0 - solid circle.
    :type line_width: int
    :param check_for_area_bounds: Whether to check if the area of the circle lies within the given constraints;
                                  defaults to False.
    :type check_for_area_bounds: bool

    :raises BodyAreaError: Size of the circle should be within the given body size constraints, if being
                                      checked.
    """
    if check_for_area_bounds:
        area: float = pi * radius ** 2

        if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
            raise exceptions.BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    pygame.draw.circle(display.get_display().surface(), color.as_tuple(), center.as_tuple(), radius, line_width)


def draw_polygon(vertices: list[Vector2D], color: Color = Color(255, 80, 80), line_width: int = 0,
                 check_for_area_bounds: bool = False) -> None:
    """
    Draw a polygon onto the display directly.

    :param vertices: Vertices describing the polygon.
    :type vertices: list[Vector2D]
    :param color: Color of the polygon; defaults to (R: 255, G: 80, B: 80) - dark red.
    :type color: Color
    :param line_width: Width of the line of the polygon; defaults to 0 - solid polygon.
    :type line_width: int
    :param check_for_area_bounds: Whether to check if the area of the polygon lies within the given constraints;
                                  defaults to False.
    :type check_for_area_bounds: bool

    :raises BodyAreaError: Size of the polygon should be within the given body size constraints, if being
                                      checked.
    """
    if check_for_area_bounds:
        # TODO: Add error checking for area.
        raise NotImplementedError('Add error checking for area.')

        if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
            raise BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    pygame.draw.polygon(
        display.get_display().surface(), color.as_tuple(), [vertex.as_tuple() for vertex in vertices], line_width
    )
