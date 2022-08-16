# TODO: Add tests.
"""
Images in Forge.
"""
from __future__ import annotations

import copy
import dataclasses

import pygame

import forge.core.engine.constants
import forge.core.engine.renderer
import forge.core.engine.settings
import forge.core.physics.vector
import forge.core.utils.aliases
import forge.core.utils.base
import forge.core.utils.dispatch

_IMAGES: dict[str, Image] = {}


@dataclasses.dataclass(slots=True)
class Image(forge.core.utils.base.Renderable):
    """
    Forge's representation of a unique image.
    """
    name: str
    filename: str
    position: forge.core.physics.vector.Vector2D

    def __post_init__(self) -> None:
        """
        Check whether the supplied image name is unique and not taken by another existing image. If unique, add the
        image to the dictionary. Also add the image to the base object renderer if the auto-add setting is enabled.

        :raises ValueError: All image names must be unique.
        """
        if self.name in _IMAGES:
            raise ValueError(f'Cannot create two images of the same name: {self.name}.')

        # Add the image to the dictionary.
        _IMAGES[self.name] = self

        # Add the image to the renderer.
        if forge.core.engine.settings.AUTO_ADD_IMAGES:
            self.add_to_renderer()

    def __repr__(self) -> str:
        """
        Internal representation of the image.

        :return: Simple string with image name and position.
        :rtype: str
        """
        return f'Image -> Name: {self.name}, Position: {self.position.__repr__()}'

    def __str__(self) -> str:
        """
        String representation of the image.

        :return: Detailed string with image information.
        :rtype: str
        """
        return f'Forge Image -> Name: {self.name}, Filename: {self.filename}, Position: {self.position.__str__()}'

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_OBJECT_RENDERER) -> None:
        """
        Add the image to a renderer.

        :param renderer_name: Name of the renderer to which the image is to be added; defaults to the base object
                              renderer.
        :type renderer_name: str
        """
        forge.core.engine.renderer.get_renderer(renderer_name).image_pool += self

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the Forge image as a Pygame surface to the display at its given position.

        :param display: Display to which the image is to be rendered.
        :type display: core.utils.aliases.Surface
        """
        display.blit(self.as_pygame_surface(), self.position.as_tuple())

    def as_pygame_surface(self) -> forge.core.utils.aliases.Surface:
        """
        Return the image as a Pygame surface. Beneficial for internal interoperability with Pygame.

        :return: Pygame surface containing the image data without the position.
        :rtype: core.utils.aliases.Surface
        """
        return pygame.image.load(self.filename)


@dataclasses.dataclass(slots=True)
class ImagePool(forge.core.utils.base.Renderable):
    """
    Forge's image pool utility.
    """
    name: str
    _images: list[Image] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Check whether the supplied pool name is unique and not taken by another existing pool. If unique, add the
        images to the dictionary. Also add the images to the base object renderer if the auto-add setting is enabled.

        :raises ValueError: All image names must be unique.
        """
        for name in _IMAGES:
            if self.name in name:
                raise ValueError(f'Cannot create two image pools of the same name.')

        # Add the images to the dictionary with the image pool prefix.
        for image in self._images:
            self._add_image_to_dictionary(image)

        # Add the images to the renderer.
        if forge.core.engine.settings.AUTO_ADD_IMAGES:
            self.add_to_renderer()

    @forge.core.utils.dispatch.multidispatch(Image)
    def __iadd__(self, image: Image) -> ImagePool:
        """
        Add an image to the pool using the '+=' operator.

        :param image: Image to be added.
        :type image: Image

        :return: Image pool with the image added to its internal list and global dictionary.
        :rtype: ImagePool

        :raises ValueError: All images in the pool must be unique.
        """
        if image in self._images:
            raise ValueError(f'Image {image} is already a part of the image pool.')

        # First, delete the image from the dictionary as a stand-alone image.
        # Then, add the image back into the dictionary but this time, as part of a pool, with its prefix.
        # Finally, add the image to the pools internal list of images.
        delete_image(image.name)
        self._add_image_to_dictionary(image)
        self._images.append(image)

        return self

    @forge.core.utils.dispatch.multidispatch(list)
    def __iadd__(self, images: list[Image]) -> ImagePool:
        """
        Add a list of images to the pool using the '+=' operator.

        :param images: List of images to be added.
        :type images: list[Image]

        :return: Image pool with the images added to its internal list and global dictionary.
        :rtype: ImagePool

        :raises ValueError: All images in the pool must be unique.
        """
        for image in images:
            if image in self._images:
                raise ValueError(f'Image {image} is already a part of the image pool.')

            # First, delete the image from the dictionary as a stand-alone image.
            # Then, add the image back into the dictionary but this time, as part of a pool, with its prefix.
            # Finally, add the image to the pools internal list of images.
            delete_image(image.name)
            self._add_image_to_dictionary(image)
            self._images.append(image)

        return self

    def __isub__(self, image: Image) -> ImagePool:
        """
        Remove an image from the pool using the '-=' operator.

        :param image: Image to be removed.
        :type image: Image

        :return: Image pool with the image removed from its internal list and global dictionary.
        :rtype: ImagePool

        :raises ValueError: Image must be part of the pool to be removed.
        """
        if image not in self._images:
            raise ValueError(f'Image {image} was never a part of the image pool.')

        image_name = f'<{self.name}-image-pool>|{image.name}'

        # First, remove the image from the pool's internal list of images.
        # Then, remove the image from the dictionary.
        # The Python garbage collector should take care of the rest.
        self._images.remove(image)
        _IMAGES.pop(image_name)

        return self

    def __repr__(self) -> str:
        """
        Internal representation of the image.

        :return: Simple string with pool name and image count.
        :rtype: str
        """
        return f'Image Pool -> Name: {self.name}, Image Count: {len(self._images)}'

    def __str__(self) -> str:
        """
        String representation of the image.

        :return: Detailed string with image pool information.
        :rtype: str
        """
        return f'Forge Image Pool -> Name: {self.name}, Dictionary Prefix: <{self.name}-image-pool>, ' \
               f'Images: {self._images}'

    def images(self) -> list[Image]:
        """
        Return the images of the pool.

        :return: List of images stored within the image pool.
        :rtype: list[Image]
        """
        return copy.copy(self._images)

    def add_to_renderer(self, renderer_name: str = forge.core.engine.constants.DISPLAY_OBJECT_RENDERER) -> None:
        """
        Add the image pool to a renderer.

        :param renderer_name: Name of the renderer to which the image pool is to be added; defaults to the base object
                              renderer.
        :type renderer_name: str
        """
        forge.core.engine.renderer.get_renderer(renderer_name).image_pool += self._images

    def _add_image_to_dictionary(self, image: Image) -> None:
        """
        Add the image to the global images dictionary with a prefix containing the name of the pool to which it belongs.

        :param image: Image to be added.
        :type image: Image
        """
        # Each image pool has a dedicated prefix so that it is easy to identify whether
        # an image belongs to a specific pool within a single dictionary without excessive
        # nesting or complication. This also allows for images with the same name to be saved
        # in two different pools without any mental overhead.
        dict_prefix = f'<{self.name}-image-pool>'

        image_name = f'{dict_prefix}|{image.name}'
        _IMAGES[image_name] = Image(image_name, image.filename, image.position)


def get_image(image_name: str, pool_name: str = '') -> Image:
    """
    Get a particular image which may either be a standalone image or part of a pool.

    :param image_name: Name of the image to retrieve.
    :type image_name: str
    :param pool_name: Name of the pool, if any; defaults to an empty string.
    :type pool_name: str

    :return: Forge image, if it exists.
    :rtype: Image

    :raises KeyError: An image must be registered if it is to be retrieved.
    """
    stored_image_name: str = image_name

    if pool_name:
        stored_image_name = f'<{pool_name}-image-pool>|{image_name}'

    if stored_image_name not in _IMAGES:
        raise KeyError(f'Image named: {stored_image_name} has not been registered as an image and cannot be retrieved.')

    return _IMAGES[stored_image_name]


def delete_image(image_name: str, pool_name: str = '') -> None:
    """
    Delete a particular image which may either be a standalone image or part of a pool.

    :param image_name: Name of the image to delete.
    :type image_name: str
    :param pool_name: Name of the pool, if any; defaults to an empty string.
    :type pool_name: str

    :raises KeyError: An image must be registered if it is to be deleted.
    """
    stored_image_name: str = image_name

    if pool_name:
        stored_image_name = f'<{pool_name}-image-pool>|{image_name}'

    if stored_image_name not in _IMAGES:
        raise KeyError(f'Image named: {stored_image_name} has not been registered as an image and cannot be deleted.')

    _IMAGES.pop(stored_image_name)


def get_images(pool_name: str) -> list[Image]:
    """
    Get all the images from a particular image pool.

    :param pool_name: Name of the pool to which the images belong.
    :type pool_name: str

    :return: List of images belonging to that pool.
    :rtype: list[Image]

    :raises ResourceWarning: A pool of the given name must ideally exist otherwise, the returned list will be empty.
    """
    images: list[Image] = []

    for image_name in _IMAGES:
        if pool_name in image_name:
            images.append(_IMAGES[image_name])

    if not images:
        raise ResourceWarning(f'A pool of the given name: {pool_name} does not exist.')

    return images


def delete_images(pool_name: str) -> None:
    """
    Delete all the images from a particular image pool.

    :param pool_name: Name of the pool to which the images belong.
    :type pool_name: str

    :raises ResourceWarning: A pool of the given name must ideally exist otherwise in effect, no images will be deleted.
    """
    num_images_popped = 0

    for image_name in _IMAGES:
        if pool_name in image_name:
            _IMAGES.pop(image_name)
            num_images_popped += 1

    if not num_images_popped:
        raise ResourceWarning(f'A pool of the given name: {pool_name} does not exist.')
