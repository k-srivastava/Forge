"""Function to check if a point is within particular bounds."""
from math import pi

from forge.core.physics import vector
from forge.core.physics.vector import Vector2D
from forge.core.physics.world import MAX_BODY_AREA, MIN_BODY_AREA
from forge.core.utils.exceptions import BodyAreaError


def point_within_rectangle(point: Vector2D, top_left: Vector2D, width: int, height: int, rotation: float = 0) -> bool:
    """
    Check if a point lies within the bounds of a rectangle.

    :param point: Point to check for bounds.
    :type point: Vector2D
    :param top_left: Top-left of the rectangle.
    :type top_left: Vector2D
    :param width: Width of the rectangle.
    :type width: int
    :param height: Height of the rectangle.
    :type height: int
    :param rotation: Rotation of the rectangle.
    :type rotation: float

    :return: True if the point lies within the bounds of the rectangle; else False.
    :rtype: bool

    :raises BodyAreaError: Size of the rectangle should be within the given body size constraints.
    """
    area: int = width * height

    if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
        raise BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    if rotation == 0:
        x_axis: bool = top_left.x <= point.x <= top_left.x + width
        y_axis: bool = top_left.y <= point.y <= top_left.y + height

        return x_axis and y_axis

    else:
        # TODO: Implement collision detection for non-aligned rectangles.
        raise NotImplementedError('Add rotated angle exceptions.')


def point_within_circle(point: Vector2D, center: Vector2D, radius: int) -> bool:
    """
    Check if a point lies within the bounds of a circle.

    :param point: Point to check for bounds.
    :type point: Vector2D
    :param center: Center of the circle.
    :type center: Vector2D
    :param radius: Radius of the circle.
    :type radius: int

    :return: True if the point lies within the bounds of the circle; else False.
    :rtype: bool

    :raises BodyAreaError: Size of the circle should be within the given body size constraints.
    """
    area: float = pi * radius ** 2

    if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
        raise BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    return vector.distance_squared_between(point, center) <= radius ** 2


def point_within_polygon(point: Vector2D, vertices: list[Vector2D], check_for_area_bounds: bool = False) -> bool:
    """
    Check if a point lies within the bounds of a polygon.

    :param point: Point to check for bounds.
    :type point: Vector2D
    :param vertices: Vertices describing the polygon.
    :type vertices: list[Vector2D]
    :param check_for_area_bounds: Whether to check if the area of the polygon lies within the given constraints;
                                  defaults to False.
    :type check_for_area_bounds: bool

    :return: True if the point lies within the bounds of the polygon; else False.
    :rtype: bool

    :raises BodyAreaError: Size of the polygon should be within the given body size constraints, if being
                                      checked.
    """
    # TODO: Implement bounds-checking for a polygon.
    raise NotImplementedError('Polygon bounds not implemented.')
