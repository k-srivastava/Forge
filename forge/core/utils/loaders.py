"""
Loaders for various assets in Forge.
"""
import os

import forge.core.engine.sprite


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
