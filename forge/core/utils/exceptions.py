"""
Custom exceptions in Forge.
"""


class IDNotFoundError(Exception):
    """
    ID has not been registered for a Forge object.
    """

    def __init__(self, id_: int) -> None:
        super().__init__(f'ID: {id_} has not been registered as an ID.')


class RGBAColorError(Exception):
    """
    Invalid RGBA color arguments.
    """

    def __init__(self, red: int, blue: int, green: int, alpha: int) -> None:
        super().__init__(
            f'RGBA colors can only have values between 0 and 255 (inclusive), not: {red, green, blue, alpha}.'
        )


class ClampError(Exception):
    """
    Values passed to be clamped are logically incorrect.
    """

    def __init__(self) -> None:
        super().__init__('The minimum bound cannot be greater than the maximum bound.')


class BodyAreaError(Exception):
    """
    Body size does not comply with specified world limits.
    """

    def __init__(self, area: float, min_body_area: float, max_body_area: float) -> None:
        super().__init__(
            f'The area is not within the specified world limits. Area must be between {min_body_area} and '
            f'{max_body_area}, not {area}.'
        )


class BodyDensityError(Exception):
    """
    Body density does not comply with specified world limits.
    """

    def __init__(self, density: float, min_body_density: float, max_body_density: float) -> None:
        super().__init__(
            f'The density is not within the specified world limits. Density must be between {min_body_density} and '
            f'{max_body_density}, not {density}.'
        )


class EventNameError(Exception):
    """
    Event with the given name already exists.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class EventNotRegisteredError(Exception):
    """
    Event with the given name or ID has not been registered.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InternalEventRetrievalError(Exception):
    """
    Internal events cannot be retrieved using their names.
    """

    def __init__(self, event_name: str) -> None:
        super().__init__(f'Event named: {event_name} is an internal event and cannot be retrieved.')


class InternalEventDeletionError(Exception):
    """
    Internal events cannot be deleted using their names.
    """

    def __init__(self, event_name: str) -> None:
        super().__init__(f'Event named: {event_name} is an internal event and cannot be deleted.')
