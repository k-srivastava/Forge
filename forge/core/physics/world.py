"""
Game environment in Forge.
"""
from forge.core.utils.exceptions import BodyAreaError, BodyDensityError

# Constraints on the body sizes.
MIN_BODY_AREA: float = 5 * 5
MAX_BODY_AREA: float = 2000 * 2000

# Constraints on the body densities.
MIN_BODY_DENSITY: float = 0.25
MAX_BODY_DENSITY: float = 25


def verify_body_constraints(area: float, density: float) -> None:
    """
    Verify that a given body fits within Forge's world constraints of a certain area and density.

    :param area: Area of the body.
    :type area: float
    :param density: Density of the body.
    :type density: float

    :raises forge.core.utils.exceptions.BodyAreaError: The body's area must lie within the world constraints.
    :raises forge.core.utils.exceptions.BodyDensityError: The body's density must lie within given world constraints.
    """
    if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
        raise BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    if not MIN_BODY_DENSITY <= area <= MAX_BODY_DENSITY:
        raise BodyDensityError(density, MIN_BODY_DENSITY, MAX_BODY_DENSITY)
