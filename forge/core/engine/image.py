"""
Images in Forge.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Self
from warnings import warn

import attrs
import pygame

from forge.core.engine import renderer
from forge.core.physics.vector import Vector2D
from forge.core.utils import dispatch, id
from forge.core.utils.aliases import Surface
from forge.core.utils.base import Renderable

_IMAGES: dict[int, 'Image'] = {}
IMAGE_IDS: dict[str, int] = {}

_IMAGE_POOLS: dict[int, 'ImagePool'] = {}
IMAGE_POOL_IDS: dict[str, int] = {}


@dataclass(slots=True)
class Image(Renderable):
    """
    Forge's representation of a unique image.
    """
    filename: str
    position: Vector2D
    name: str = attrs.field(on_setattr=attrs.setters.frozen)
    parent: Optional[ImagePool] = field(default=None, init=False)
    _id: int = field(init=False)

    def __post_init__(self) -> None:
        """
        Check whether the supplied image name is unique and not taken by another existing image. If unique, add the
        image to the dictionary. Also create a new unique ID for the image.

        :raises ValueError: All image names must be unique.
        """
        if self.name in IMAGE_IDS:
            raise ValueError(f'Cannot create two images of the same name: {self.name}.')

        self._id = id.generate_random_id()

        _IMAGES[self._id] = self
        IMAGE_IDS[self.name] = self._id

    def id(self) -> int:
        """
        Get the unique ID of the image.

        :return: ID of the image.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self) -> None:
        """
        Add the image to a renderer.
        """
        renderer.get_master_renderer().add_image(self)

    def render(self, display: Surface) -> None:
        """
        Render the Forge image as a Pygame surface to the display at its given position.

        :param display: Display to which the image is to be rendered.
        :type display: core.utils.aliases.Surface
        """
        display.blit(self.as_pygame_surface(), self.position.as_tuple())

    def as_pygame_surface(self) -> pygame.surface.Surface:
        """
        Return the image as a Pygame surface. Beneficial for internal interoperability with Pygame.

        :return: Pygame surface containing the image data without the position.
        :rtype: pygame.surface.Surface
        """
        return pygame.image.load(self.filename).convert_alpha()


@dataclass(slots=True)
class ImagePool(Renderable):
    """
    Forge's image pool utility.
    """
    name: str = attrs.field(on_setattr=attrs.setters.frozen)
    _id: int = field(init=False)
    _images: list[Image] = field(default_factory=list)
    _belongs_to_renderer: bool = False

    def __post_init__(self) -> None:
        """
        Check whether the supplied pool name is unique and not taken by another existing pool. If unique, add the
        images to the dictionary. Also create a new unique ID for the image pool.

        :raises ValueError: All image pool names must be unique.
        """
        if self.name in IMAGE_POOL_IDS:
            raise ValueError(f'Cannot create two image pools of the same name: {self.name}.')

        self._id = id.generate_random_id()

        _IMAGE_POOLS[self._id] = self
        IMAGE_POOL_IDS[self.name] = self._id

        if not self._belongs_to_renderer:
            for image in self._images:
                image.parent = self

    @dispatch.multidispatch(Image)
    def __iadd__(self, image: Image) -> Self:
        """
        Add an image to the pool using the '+=' operator.

        :param image: Image to be added.
        :type image: Image

        :return: Image pool with the image added to its internal list.
        :rtype: Self

        :raises ValueError: All images in the pool must be unique.
        """
        if image.parent == self:
            warn(f'Image {image.name} is already part of the pool.')
            return self

        if not self._belongs_to_renderer:
            image.parent = self
            renderer.get_master_renderer().add_image(image)

        self._images.append(image)
        return self

    @dispatch.multidispatch(list)
    def __iadd__(self, images: list[Image]) -> Self:
        """
        Add a list of images to the pool using the '+=' operator.

        :param images: List of images to be added.
        :type images: list[Image]

        :return: Image pool with the images added to its internal list.
        :rtype: Self

        :raises ValueError: All images in the pool must be unique.
        """
        for image in images:
            if image.parent == self:
                warn(f'Image {image.name} is already part of the pool.')
                continue

            if not self._belongs_to_renderer:
                image.parent = self
                renderer.get_master_renderer().add_image(image)

            self._images.append(image)

        return self

    @dispatch.multidispatch(Image)
    def __isub__(self, image: Image) -> Self:
        """
        Remove an image from the pool using the '-=' operator.

        :param image: Image to be removed.
        :type image: Image

        :return: Image pool with the image removed from its internal list.
        :rtype: Self

        :raises ValueError: Image must be part of the pool to be removed.
        """
        # A no-inspection is used because all overloaded functions will be re-written from scratch.
        # noinspection DuplicatedCode
        if self._belongs_to_renderer:
            self._images.remove(image)
            return self

        if image.parent != self:
            raise ValueError(f'Image {image.name} was never part of the pool.')

        image.parent = None

        self._images.remove(image)
        renderer.get_master_renderer().remove_image(image)

        return self

    @dispatch.multidispatch(str)
    def __isub__(self, image_data: str | int) -> Self:
        image: Image
        if type(image_data) is str:
            image = get_image_from_name(image_data)
        else:
            image = get_image_from_id(image_data)

        # A no-inspection is used because all overloaded functions will be re-written from scratch.
        # noinspection DuplicatedCode
        if self._belongs_to_renderer:
            self._images.remove(image)
            return self

        if image.parent != self:
            raise ValueError(f'Image {image.name} was never part of the pool.')

        image.parent = None

        self._images.remove(image)
        renderer.get_master_renderer().remove_image(image)

        return self

    def id(self) -> int:
        """
        Get the unique ID of the image pool.

        :return: ID of the image pool.
        :rtype: int
        """
        return self._id

    def images(self) -> list[Image]:
        """
        Return the images of the pool.

        :return: List of images stored within the image pool.
        :rtype: list[Image]
        """
        return self._images.copy()

    def add_to_renderer(self) -> None:
        """
        Add the image pool to its renderer.
        """
        renderer.get_master_renderer().add_images(self._images)

    def render(self, display: Surface) -> None:
        """
        For each Forge image in the pool, render it as a Pygame surface to the display at its given position.

        :param display: Display to which the image pool is to be rendered.
        :type display: Surface
        """
        for image in self._images:
            image.render(display)

    def as_pygame_surfaces(self) -> list[pygame.surface.Surface]:
        """
        Return the image pool as a list Pygame surfaces. Beneficial for internal interoperability with Pygame.

        :return: List of Pygame surfaces containing the image data without the position.
        :rtype: list[pygame.surface.Surface]
        """
        return [pygame.image.load(image.filename).convert_alpha() for image in self._images]


# A no-inspection is used because all overloaded functions will be re-written from scratch.
# noinspection DuplicatedCode
def get_image_from_name(image_name: str) -> Image:
    """
    Retrieve a registered image from the image dictionary using the image name.

    :param image_name: Name of the image to be retrieved.
    :type image_name: str

    :return: Image stored in the image dictionary.
    :rtype: Image

    :raises KeyError: An image must be registered if it is to be retrieved.
    """
    if image_name not in IMAGE_IDS:
        raise KeyError(f'Image named: {image_name} has not been registered as an image and cannot be retrieved.')

    return _IMAGES[IMAGE_IDS[image_name]]


def get_image_from_id(image_id: int) -> Image:
    """
    Retrieve a registered image from the image dictionary using the image ID.

    :param image_id: ID of the image to be retrieved.
    :type image_id: int

    :return: Image stored in the image dictionary.
    :rtype: Image

    :raises KeyError: An image must be registered if it is to be retrieved.
    """
    if image_id not in _IMAGES:
        raise KeyError(f'Image with ID: {image_id} has not been registered as an image and cannot br retrieved.')

    return _IMAGES[image_id]


def delete_image_from_name(image_name: str) -> None:
    """
    Delete a registered image from the image dictionary using the image name and free the ID of the image.

    :param image_name: Name of the image to be deleted.
    :type image_name: str

    :raises KeyError: An image must be registered if it is to be deleted.
    """
    if image_name not in IMAGE_IDS:
        raise KeyError(f'Image named: {image_name} has not been registered as an image and cannot be deleted.')

    _IMAGES.pop(IMAGE_IDS[image_name])
    id.delete_id(IMAGE_IDS[image_name])
    IMAGE_IDS.pop(image_name)


def delete_image_from_id(image_id: int) -> None:
    """
    Delete a registered image from the image dictionary using the image ID and free the ID of the image.

    :param image_id: ID of the image to be deleted.
    :type image_id: int

    :raises KeyError: An image must be registered if it is to be deleted.
    """
    if image_id not in _IMAGES:
        raise KeyError(f'Image with ID: {image_id} has not been registered as an image and cannot be deleted.')

    image_name = _IMAGES.pop(image_id).name
    id.delete_id(image_id)
    IMAGE_IDS.pop(image_name)


# A no-inspection is used because all overloaded functions will be re-written from scratch.
# noinspection DuplicatedCode
def get_image_pool_from_name(image_pool_name: str) -> ImagePool:
    """
    Retrieve a registered image pool from the image pool dictionary using the image pool name.

    :param image_pool_name: Name of the image pool to be retrieved.
    :type image_pool_name: str

    :return: Image pool stored in the internal dictionary.
    :rtype: ImagePool

    :raises KeyError: An image pool must be registered if it is to be retrieved.
    """
    if image_pool_name not in IMAGE_POOL_IDS:
        raise KeyError(
            f'Image pool named: {image_pool_name} has not been registered as an image pool and cannot be retrieved.'
        )

    return _IMAGE_POOLS[IMAGE_POOL_IDS[image_pool_name]]


def get_image_pool_from_id(image_pool_id: int) -> ImagePool:
    """
    Retrieve a registered image pool from the image pool dictionary using the image pool ID.

    :param image_pool_id: ID of the image pool to be retrieved.
    :type image_pool_id: int

    :return: Forge image pool stored in the internal dictionary.
    :rtype: ImagePool

    :raises KeyError: An image pool must be registered if it is to be retrieved.
    """
    if image_pool_id not in _IMAGE_POOLS:
        raise KeyError(
            f'Image pool with ID: {image_pool_id} has not been registered as an image pool and cannot be retrieved.'
        )

    return _IMAGE_POOLS[image_pool_id]


def delete_image_pool_from_name(image_pool_name: str) -> None:
    """
    Delete a registered image pool from the image pool dictionary using the image pool name and free the ID of the
    image pool.

    :param image_pool_name: Name of the image pool to be deleted.
    :type image_pool_name: str

    :raises KeyError: An image pool must be registered if it is to be deleted.
    """
    if image_pool_name not in IMAGE_POOL_IDS:
        raise KeyError(
            f'Image pool named: {image_pool_name} has not been registered as an image pool and cannot be deleted.'
        )

    _IMAGE_POOLS.pop(IMAGE_POOL_IDS[image_pool_name])
    id.delete_id(IMAGE_POOL_IDS[image_pool_name])
    IMAGE_POOL_IDS.pop(image_pool_name)


def delete_image_pool_from_id(image_pool_id: int) -> None:
    """
    Delete a registered image pool from the image pool dictionary using the image pool ID and free the ID of the image
    pool.

    :param image_pool_id: ID of the image pool to be deleted.
    :type image_pool_id: int

    :raises KeyError: An image pool must be registered if it is to be deleted.
    """
    if image_pool_id not in _IMAGE_POOLS:
        raise KeyError(
            f'Image pool with ID: {image_pool_id} has not been registered as an image pool and cannot be deleted.'
        )

    image_pool_name = _IMAGE_POOLS.pop(image_pool_id).name
    id.delete_id(image_pool_id)
    IMAGE_POOL_IDS.pop(image_pool_name)
