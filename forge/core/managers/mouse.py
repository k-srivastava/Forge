"""
Forge's direct wrapping for Pygame's mouse.
"""
import enum

import pygame

import forge.core.engine.game
import forge.core.physics.vector

DISABLED = False


class MouseButton(enum.Enum):
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

    game = forge.core.engine.game.get_game()

    if game is not None:
        for event in game.event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Disabling the type-checker because the MouseButton enum will only have integer values that are
                # tuple-compatible.
                # noinspection PyTypeChecker
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

    game = forge.core.engine.game.get_game()

    if game is not None:
        for event in game.event_list:
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

    # Disabling the type-checker because the MouseButton enum will only have integer values that are tuple-compatible.
    # noinspection PyTypeChecker
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


def position() -> forge.core.physics.vector.Vector2D:
    """
    Get the current mouse position as a vector.

    :return: Current mouse position.
    :rtype: core.physics.vector.Vector2D
    """
    if DISABLED:
        return forge.core.physics.vector.zero()

    return forge.core.physics.vector.from_tuple(pygame.mouse.get_pos())


def movement() -> forge.core.physics.vector.Vector2D:
    """
    Get the relative position, or movement, of the mouse as a vector.

    :return: Relative mouse position.
    :rtype: core.physics.vector.Vector2D
    """
    if DISABLED:
        return forge.core.physics.vector.zero()

    return forge.core.physics.vector.from_tuple(pygame.mouse.get_rel())


def modify_visibility(visible: bool) -> None:
    """
    Change the visibility of the mouse on the display.

    :param visible: Whether the mouse should be made visible or not.
    :type visible: bool
    """
    if not DISABLED:
        pygame.mouse.set_visible(visible)
