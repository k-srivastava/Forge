"""
Basic state management in Forge.
"""
import typing

import forge.core.utils.id

_STATE_VARIABLES: dict[int, int | float | str | bool] = {}


@typing.overload
def create_state_variable(value: int) -> tuple[typing.Callable[[], int], typing.Callable[[int], None]]:
    """
    Overload for the base method for integer state variables.

    :type value: int
    :rtype: tuple[typing.Callable[[], int], typing.Callable[[int], None]]
    """


@typing.overload
def create_state_variable(value: float) -> tuple[typing.Callable[[], float], typing.Callable[[float], None]]:
    """
    Overload for the base method for floating-point state variables.

    :type value: float
    :rtype: tuple[typing.Callable[[], float], typing.Callable[[float], None]]
    """


@typing.overload
def create_state_variable(value: str) -> tuple[typing.Callable[[], str], typing.Callable[[str], None]]:
    """
    Overload for the base method for string state variables.

    :type value: str
    :rtype: tuple[typing.Callable[[], str], typing.Callable[[str], None]]
    """


@typing.overload
def create_state_variable(value: bool) -> tuple[typing.Callable[[], bool], typing.Callable[[bool], None]]:
    """
    Overload for the base method for boolean state variables.

    :type value: bool
    :rtype: tuple[typing.Callable[[], bool], typing.Callable[[bool], None]]
    """


def create_state_variable(value):
    """
    Create a new state variable with an initial value.

    :param value: Initial value of the state variable.

    :return: Getter and setter methods for the state variable.
    """
    variable_id = forge.core.utils.id.generate_random_id()
    _STATE_VARIABLES[variable_id] = value

    def getter():
        return _STATE_VARIABLES[variable_id]

    def setter(new_value):
        _STATE_VARIABLES[variable_id] = new_value

    return getter, setter
