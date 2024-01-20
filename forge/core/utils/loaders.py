"""
Loaders for various assets in Forge.
"""
import os

from forge.core.engine.sprite import Sprite
from forge.core.managers.event import Event, INTERNAL_EVENT_NAMES, InternalEvent


def load_sprites_from_folders(path: str) -> list[Sprite]:
    """
    Load files from various nested sub-folders as Forge sprites.

    :param path: Base or parent folder path.
    :type path: str

    :return: List of all sprites loaded from the sub-folders.
    :rtype: list[Sprite]
    """
    sprites: list[Sprite] = []

    for _, _, image_files in os.walk(path):
        for image_file in image_files:
            file_path = f'{path}/{image_file}'
            sprites.append(Sprite(file_path))

    return sprites


def load_internal_events(*skip_events: InternalEvent) -> None:
    """
    Load all internal Forge events.

    :param skip_events: Enum names of internal events to be skipped during the loading.
    :type: InternalEvent
    """
    internal_events: list[InternalEvent] = [
        InternalEvent.MOUSE_CLICKED,
        InternalEvent.MOUSE_DEPRESSED,
        InternalEvent.KEY_PRESSED
    ]

    for event in internal_events:
        # The corresponding value for the enum will always be a string.
        # noinspection PyTypeHints
        event.value: str

        if event in skip_events:
            continue

        Event(event.value)
        INTERNAL_EVENT_NAMES.append(event.value)
