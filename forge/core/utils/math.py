"""
Core mathematical functions for Forge.
"""


def clamp(value: int | float, min_: int | float, max_: int | float) -> int | float:
    """
    Clamp a value between a specified minimum and maximum bound.

    :param value: Value to be clamped.
    :type value: int | float
    :param min_: Minimum bound of the clamp.
    :type min_: int | float
    :param max_: Maximum bound of the clamp.
    :type max_: int | float

    :return: Value to be clamped to the minimum and maximum bound.
    :rtype: int | float

    :raises ValueError: The maximum bound cannot be greater than the minimum bound.
    """
    if min_ > max_:
        raise ValueError('The minimum bound cannot be greater than the maximum bound.')

    if value > max_:
        value = max_

    elif value < min_:
        value = min_

    return value
