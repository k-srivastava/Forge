"""
Game environment in Forge.
"""
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

    :raises ValueError: The body's area and density must lie within the given world constraints.
    """
    if not MIN_BODY_AREA <= area <= MAX_BODY_AREA:
        raise ValueError(
            f'The area is not within the specified world limits. Area must be between {MIN_BODY_AREA} and '
            f'{MAX_BODY_AREA}, not {area}.'
        )

    if not MIN_BODY_DENSITY <= area <= MAX_BODY_DENSITY:
        raise ValueError(
            f'The density is not within the specified world limits. Density must be between {MIN_BODY_DENSITY} and '
            f'{MAX_BODY_DENSITY}, not {density}.'
        )
