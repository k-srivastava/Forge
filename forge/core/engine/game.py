"""
Base game for Forge.
"""
from __future__ import annotations

from typing import Optional

import pygame

from forge.core.engine.display import Display
from forge.core.managers import event, keyboard, mouse
from forge.core.managers.event import InternalEvent
from forge.core.utils import loaders

# Store the current game in a list of length one.
# A list has to be used because a global variable becomes lengthy to implement.
_GAME: list[Optional[Game]] = [None]


class Game:
    """
    Base game class in Forge that handles the display management and event loop.
    """

    def __init__(self, display: Display) -> None:
        """
        Initialize the Forge game.

        :param display: Display for the game.
        :type display: Display

        :raises RuntimeError: Only one game can be created at a time.
        """
        if _GAME[0] is not None:
            raise RuntimeError('New game cannot be created when one already exists.')

        pygame.init()

        self.display = display
        self.event_list: Optional[list[pygame.event.Event]] = None

        loaders.load_internal_events()

        _GAME[0] = self

    def mainloop(self) -> None:
        """
        Main loop of the game.
        """
        while True:
            self.event_list = pygame.event.get()
            self.event_handler()

    def event_handler(self) -> None:
        """
        Event handler for the game. Handles all the native Pygame events and exits the loop when the window is closed.
        """
        for event_ in self.event_list:
            if event_.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            elif event_.type == pygame.MOUSEBUTTONDOWN and not mouse.DISABLED:
                event.get_internal_event(
                    InternalEvent.MOUSE_CLICKED
                ).post()

            elif event_.type == pygame.KEYDOWN and not keyboard.DISABLED:
                event.get_internal_event(
                    InternalEvent.KEY_PRESSED
                ).post()

        if any(pygame.mouse.get_pressed()) and not mouse.DISABLED:
            event.get_internal_event(InternalEvent.MOUSE_DEPRESSED).post()

        if any(pygame.key.get_pressed()) and not keyboard.DISABLED:
            event.get_internal_event(InternalEvent.KEY_PRESSED).post()

        self.update()
        self.render()

    def render(self) -> None:
        """
        Render the game's display.
        """
        self.display.render()

    def update(self) -> None:
        """
        Update the game and its display.
        """
        self.display.update()


def get_game() -> Optional[Game]:
    """
    Retrieve the current game.

    :return: Current game; if it exists.
    :rtype: Optional[Game]
    """
    return _GAME[0]
