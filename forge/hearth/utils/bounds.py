"""
Functions to check if a point is within particular bounds.
"""
import forge.core.physics.vector


def point_within_rectangle(
        point: forge.core.physics.vector.Vector2D,
        top_left: forge.core.physics.vector.Vector2D, width: int, height: int
) -> bool:
    """
    Check if a point lies within the bounds of a rectangle.

    :param point: Point to check for bounds.
    :type point: forge.core.physics.vector.Vector2D
    :param top_left: Top-left of the rectangle.
    :type top_left: forge.core.physics.vector.Vector2D
    :param width: Width of the rectangle.
    :type width: int
    :param height: Height of the rectangle.
    :type height: int

    :return: True if the point lies within the bounds of the rectangle; else False.
    :rtype: bool
    """
    x_axis = top_left.x <= point.x <= top_left.x + width
    y_axis = top_left.y <= point.y <= top_left.y + height

    return x_axis and y_axis


def point_within_circle(
        point: forge.core.physics.vector.Vector2D,
        center: forge.core.physics.vector.Vector2D, radius: int
) -> bool:
    """
    Check if a point lies within the bounds of a circle.

    :param point: Point to check for bounds.
    :type point: forge.core.physics.vector.Vector2D
    :param center: Center of the circle.
    :type center: forge.core.physics.vector.Vector2D
    :param radius: Radius of the circle.
    :type radius: int

    :return: True if the point lies within the bounds of the circle; else False.
    :rtype: bool
    """
    return forge.core.physics.vector.distance_squared_between(point, center) <= radius ** 2


def point_within_polygon(
        point: forge.core.physics.vector.Vector2D,
        vertices: list[forge.core.physics.vector.Vector2D]
) -> bool:
    """
    Check of a point lies within the bounds of a polygon.

    :param point: Point to check for bounds.
    :type point: forge.core.physics.vector.Vector2D
    :param vertices: List of vertices describing the polygon.
    :type vertices: list[forge.core.physics.vector.Vector2D]

    :return: True if the point lies within the bounds of the polygon; else False.
    :rtype: bool
    """
    # Code Source: https://stackoverflow.com/questions/22521982/check-if-point-is-inside-a-polygon
    # Essentially, check each vertex with the next vertex in the polygon (special case for last vertex which
    # is compared to the first vertex) and continuously map whether the point lies within the polygon or not.
    point_inside = False

    j = len(vertices)
    for i in range(len(vertices)):
        current_vertex = vertices[i]
        next_vertex = vertices[j]

        base_bounds = (current_vertex.y > point.y) != (next_vertex.y > point.y)
        core_bounds = point.x < (next_vertex.x - current_vertex.x) * (point.y - current_vertex.y) / (
                next_vertex.y - current_vertex.y) + current_vertex.x

        if base_bounds and core_bounds:
            point_inside = not point_inside

        # Set "j" equal to the current value of "i" before "i" is incremented at the end of each loop iteration.
        j = i

    return point_inside
