# TODO: Add tests.
"""
Images in Forge.
"""
from __future__ import annotations

import dataclasses
import warnings

import attrs
import pygame

import forge.core.engine.constants
import forge.core.engine.renderer
import forge.core.physics.vector
import forge.core.utils.aliases
import forge.core.utils.base
import forge.core.utils.dispatch
import forge.core.utils.id

_IMAGES: dict[int, Image] = {}
IMAGE_IDS: dict[str, int] = {}

_IMAGE_POOLS: dict[int, ImagePool] = {}
IMAGE_POOL_IDS: dict[str, int] = {}


@dataclasses.dataclass(slots=True)
class Image(forge.core.utils.base.Renderable):
    """
    Forge's representation of a unique image.
    """
    filename: str
    position: forge.core.physics.vector.Vector2D
    name: str = attrs.field(on_setattr=attrs.setters.frozen)
    parent: ImagePool | None = dataclasses.field(default=None, init=False)
    _id: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """
        Check whether the supplied image name is unique and not taken by another existing image. If unique, add the
        image to the dictionary. Also create a new unique ID for the image.

        :raises ValueError: All image names must be unique.
        """
        if self.name in IMAGE_IDS:
            raise ValueError(f'Cannot create two images of the same name: {self.name}.')

        self._id = forge.core.utils.id.generate_random_id()

        _IMAGES[self._id] = self
        IMAGE_IDS[self.name] = self._id

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
        return f'Forge Image -> Name: {self.name}, ID: {self._id} Filename: {self.filename}, ' \
               f'Position: {self.position.__str__()}'

    def id(self) -> int:
        """
        Get the unique ID of the image.

        :return: ID of the image.
        :rtype: int
        """
        return self._id

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

    def as_pygame_surface(self) -> pygame.surface.Surface:
        """
        Return the image as a Pygame surface. Beneficial for internal interoperability with Pygame.

        :return: Pygame surface containing the image data without the position.
        :rtype: pygame.surface.Surface
        """
        return pygame.image.load(self.filename).convert_alpha()


@dataclasses.dataclass(slots=True)
class ImagePool:
    """
    Forge's image pool utility.
    """
    name: str = attrs.field(on_setattr=attrs.setters.frozen)
    renderer_name: str = forge.core.engine.constants.DISPLAY_OBJECT_RENDERER
    _id: int = dataclasses.field(init=False)
    _images: list[Image] = dataclasses.field(default_factory=list)
    _belongs_to_renderer: bool = False

    def __post_init__(self) -> None:
        """
        Check whether the supplied pool name is unique and not taken by another existing pool. If unique, add the
        images to the dictionary. Also create a new unique ID for the image pool.

        :raises ValueError: All image pool names must be unique.
        """
        if self.name in IMAGE_POOL_IDS:
            raise ValueError(f'Cannot create two image pools of the same name: {self.name}.')

        self._id = forge.core.utils.id.generate_random_id()

        _IMAGE_POOLS[self._id] = self
        IMAGE_POOL_IDS[self.name] = self._id

        if not self._belongs_to_renderer:
            for image in self._images:
                image.parent = self

    @forge.core.utils.dispatch.multidispatch(Image)
    def __iadd__(self, image: Image) -> ImagePool:
        """
        Add an image to the pool using the '+=' operator.

        :param image: Image to be added.
        :type image: Image

        :return: Image pool with the image added to its internal list.
        :rtype: ImagePool

        :raises ValueError: All images in the pool must be unique.
        """
        if image.parent == self:
            warnings.warn(f'Image {image.name} is already part of the pool.')
            return self

        if not self._belongs_to_renderer:
            image.parent = self
            forge.core.engine.renderer.get_renderer(self.renderer_name).image_pool += image

        self._images.append(image)
        return self

    @forge.core.utils.dispatch.multidispatch(list)
    def __iadd__(self, images: list[Image]) -> ImagePool:
        """
        Add a list of images to the pool using the '+=' operator.

        :param images: List of images to be added.
        :type images: list[Image]

        :return: Image pool with the images added to its internal list.
        :rtype: ImagePool

        :raises ValueError: All images in the pool must be unique.
        """
        for image in images:
            if image.parent == self:
                warnings.warn(f'Image {image.name} is already part of the pool.')
                continue

            if not self._belongs_to_renderer:
                image.parent = self
                forge.core.engine.renderer.get_renderer(self.renderer_name).image_pool += image

            self._images.append(image)

        return self

    @forge.core.utils.dispatch.multidispatch(Image)
    def __isub__(self, image: Image) -> ImagePool:
        """
        Remove an image from the pool using the '-=' operator.

        :param image: Image to be removed.
        :type image: Image

        :return: Image pool with the image removed from its internal list.
        :rtype: ImagePool

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
        forge.core.engine.renderer.get_renderer(self.renderer_name).image_pool -= image

        return self

    @forge.core.utils.dispatch.multidispatch(str)
    def __isub__(self, image_data: str | int) -> ImagePool:
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
        forge.core.engine.renderer.get_renderer(self.renderer_name).image_pool -= image

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
        return f'Forge Image Pool -> Name: {self.name}, ID: {self._id}, Images: {self._images}'

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
        forge.core.engine.renderer.get_renderer(self.renderer_name).image_pool += self._images

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
    Retrieve a particular image from the image dictionary using the image name.

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
    forge.core.utils.id.delete_id(IMAGE_IDS[image_name])
    IMAGE_IDS.pop(image_name)


def delete_image_from_id(image_id: int) -> None:
    """
    Delete a registered image from the image dictionary using the image ID and free the ID of the image.

    :param image_id: ID of the image to be deleted.
    :type image_id: int

    :raises KeyError: An image must be registered if it is to be deleted.
    :param image_id:
    """
    if image_id not in _IMAGES:
        raise KeyError(f'Image with ID: {image_id} has not been registered as an image and cannot be deleted.')

    image_name = _IMAGES.pop(image_id).name
    forge.core.utils.id.delete_id(image_id)
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
    forge.core.utils.id.delete_id(IMAGE_POOL_IDS[image_pool_name])
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
    forge.core.utils.id.delete_id(image_pool_id)
    IMAGE_POOL_IDS.pop(image_pool_name)
