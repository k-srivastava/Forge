"""
Loaders for various assets in Forge.
"""
import os

import forge.core.engine.sprite
import forge.core.managers.event


def load_sprites_from_folders(path: str) -> list[forge.core.engine.sprite.Sprite]:
    """
    Load files from various nested sub-folders as Forge sprites.

    :param path: Base or parent folder path.
    :type path: str

    :return: List of all sprites loaded from the sub-folders.
    :rtype: list[forge.core.engine.sprite.Sprite]
    """
    sprites: list[forge.core.engine.sprite.Sprite] = []

    for _, _, image_files in os.walk(path):
        for image_file in image_files:
            file_path = f'{path}/{image_file}'
            sprites.append(forge.core.engine.sprite.Sprite(file_path))

    return sprites


def load_internal_events(*skip_events: forge.core.managers.event.InternalEvent) -> None:
    """
    Load all internal Forge events.

    :param skip_events: Enum names of internal events to be skipped during the loading.
    :type: forge.core.managers.event.InternalEvent
    """
    internal_events: list[forge.core.managers.event.InternalEvent] = [
        forge.core.managers.event.InternalEvent.MOUSE_CLICKED,
        forge.core.managers.event.InternalEvent.MOUSE_DEPRESSED,
        forge.core.managers.event.InternalEvent.KEY_PRESSED
    ]

    for event in internal_events:
        # The corresponding value for the enum will always be a string.
        # noinspection PyTypeHints
        event.value: str

        if event in skip_events:
            continue

        forge.core.managers.event.Event(event.value)
        forge.core.managers.event.INTERNAL_EVENT_NAMES.append(event.value)
