"""
Forge's direct wrapping for Pygame's mouse.
"""
from enum import IntEnum

import pygame

from forge.core.engine import game
from forge.core.physics import vector
from forge.core.physics.vector import Vector2D

DISABLED = False


class MouseButton(IntEnum):
    """
    Enum containing all possible mouse buttons for a simple three-buttoned mouse.
    """
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


def is_clicked(mouse_button: MouseButton) -> bool:
    """
    Check if a certain mouse button of a three-buttoned mouse is pressed once.

    :param mouse_button: Enum value of the mouse button to check.
    :type mouse_button: MouseButton

    :return: True if the mouse button passed is pressed once; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    current_game = game.get_game()

    if current_game is not None:
        for event in current_game.event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[mouse_button.value]:
                    return True

    return False


def is_any_clicked() -> bool:
    """
    Check if any mouse button of a three-buttoned mouse is pressed once.

    :return: True if any mouse button passed is pressed once; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    current_game = game.get_game()

    if current_game is not None:
        for event in current_game.event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

    return False


def is_pressed(mouse_button: MouseButton) -> bool:
    """
    Check if a certain mouse button of a three-buttoned mouse is pressed continuously.

    :param mouse_button: Enum value of the mouse button to check.
    :type mouse_button: MouseButton

    :return: True if the mouse button passed is pressed continuously; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    return pygame.mouse.get_pressed()[mouse_button.value]


def is_any_pressed() -> bool:
    """
    Check if any mouse button of a three-buttoned mouse is pressed.

    :return: True if any mouse button is pressed; else False.
    :rtype: bool
    """
    if DISABLED:
        return False

    return any(pygame.mouse.get_pressed())


def position() -> Vector2D:
    """
    Get the current mouse position as a vector.

    :return: Current mouse position.
    :rtype: Vector2D
    """
    if DISABLED:
        return Vector2D.zero()

    return vector.from_tuple(pygame.mouse.get_pos())


def movement() -> Vector2D:
    """
    Get the relative position, or movement, of the mouse as a vector.

    :return: Relative mouse position.
    :rtype: Vector2D
    """
    if DISABLED:
        return Vector2D.zero()

    return vector.from_tuple(pygame.mouse.get_rel())


def modify_visibility(visible: bool) -> None:
    """
    Change the visibility of the mouse on the display.

    :param visible: Whether the mouse should be made visible or not.
    :type visible: bool
    """
    if not DISABLED:
        pygame.mouse.set_visible(visible)
