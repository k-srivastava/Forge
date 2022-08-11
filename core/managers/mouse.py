"""
Forge's direct wrapping for Pygame's mouse.
"""
import enum

import pygame

import core.physics.vector


class MouseButton(enum.Enum):
    """
    Enum containing all possible mouse buttons for a simple three-buttoned mouse.
    """
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


def is_pressed(mouse_button: MouseButton) -> bool:
    """
    Check if a certain mouse button of a three-buttoned mouse is pressed.

    :param mouse_button: Enum value of the mouse button to check.
    :type mouse_button: MouseButton

    :return: True if the mouse button passed is pressed; else False.
    :rtype: bool
    """
    # Disabling the type-checker because the MouseButton enum will only have integer values that are tuple-compatible.
    # noinspection PyTypeChecker
    return pygame.mouse.get_pressed()[mouse_button.value]


def is_any_pressed() -> bool:
    """
    Check if any mouse button of a three-buttoned mouse is pressed.

    :return: True if any mouse button is pressed; else False.
    :rtype: bool
    """
    return any(pygame.mouse.get_pressed())


def position() -> core.physics.vector.Vector2D:
    """
    Get the current mouse position as a vector.

    :return: Current mouse position.
    :rtype: core.physics.vector.Vector2D
    """
    return core.physics.vector.from_tuple(pygame.mouse.get_pos())


def movement() -> core.physics.vector.Vector2D:
    """
    Get the relative position, or movement, of the mouse as a vector.

    :return: Relative mouse position.
    :rtype: core.physics.vector.Vector2D
    """
    return core.physics.vector.from_tuple(pygame.mouse.get_rel())


def modify_visibility(visible: bool) -> None:
    """
    Change the visibility of the mouse on the display.

    :param visible: Whether the mouse should be made visible or not.
    :type visible: bool
    """
    pygame.mouse.set_visible(visible)
