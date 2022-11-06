"""
Game environment in Forge.
"""
import forge.core.utils.exceptions

# Constraints on the body sizes.
MIN_BODY_AREA: float = 0.01 * 0.01
MAX_BODY_AREA: float = 64 * 64

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
        raise forge.core.utils.exceptions.BodyAreaError(area, MIN_BODY_AREA, MAX_BODY_AREA)

    if not MIN_BODY_DENSITY <= area <= MAX_BODY_DENSITY:
        raise forge.core.utils.exceptions.BodyDensityError(density, MIN_BODY_DENSITY, MAX_BODY_DENSITY)
