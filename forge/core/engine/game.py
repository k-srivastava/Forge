"""
Base game for Forge.
"""
from __future__ import annotations

import sys

import pygame

import forge.core.engine.display
import forge.core.managers.event
import forge.core.utils.loaders

# Store the current game in a list of length one.
# A list has to be used because a global variable becomes lengthy to implement.
_GAME: list[Game | None] = [None]


class Game:
    """
    Base game class in Forge that handles the display management and event loop.
    """

    def __init__(self, display: forge.core.engine.display.Display) -> None:
        """
        Initialize the Forge game.

        :param display: Display for the game.
        :type display: forge.core.engine.display.Display

        :raises SyntaxError: Only one game can be created at a time.
        """
        if _GAME[0] is not None:
            raise SyntaxError('New game cannot be created when one already exists.')

        pygame.init()

        self.display = display
        self.event_list: list[pygame.event.Event] | None = None

        forge.core.utils.loaders.load_internal_events()

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
        for event in self.event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                forge.core.managers.event.get_internal_event(
                    forge.core.managers.event.InternalEvent.MOUSE_CLICKED
                ).post()

        if any(pygame.mouse.get_pressed()):
            forge.core.managers.event.get_internal_event(forge.core.managers.event.InternalEvent.MOUSE_DEPRESSED).post()

        if any(pygame.key.get_pressed()):
            forge.core.managers.event.get_internal_event(forge.core.managers.event.InternalEvent.KEY_PRESSED).post()

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


def get_game() -> Game | None:
    """
    Retrieve the current game.

    :return: Current game, if it exists.
    :rtype: Game | None
    """
    return _GAME[0]
