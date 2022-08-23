"""
Renderers for Forge.
"""
from __future__ import annotations

import dataclasses

import attrs

import forge.core.engine.color
import forge.core.engine.image
import forge.core.utils.aliases
import forge.core.utils.base
import forge.core.utils.id

_RENDERERS: dict[int, Renderer] = {}
RENDERER_IDS: dict[str, int] = {}


@dataclasses.dataclass(slots=True)
class Renderer:
    name: str = attrs.field(on_setattr=attrs.setters.frozen)
    image_pool: forge.core.engine.image.ImagePool = dataclasses.field(init=False)
    _id: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        if self.name in RENDERER_IDS:
            raise ValueError(f'Cannot create two renderers of the same name: {self.name}.')

        self._id = forge.core.utils.id.generate_random_id()
        self.image_pool = forge.core.engine.image.ImagePool(self.name, _images=[], _belongs_to_renderer=True)

        _RENDERERS[self._id] = self
        RENDERER_IDS[self.name] = self._id

    def __repr__(self) -> str:
        """
        Internal representation of the renderer.

        :return: Simple string with renderer name and image count.
        :rtype: str
        """
        return f'Renderer -> Name: {self.name}, Image Count: {len(self.image_pool.images())}'

    def __str__(self) -> str:
        """
        String representation of the renderer.

        :return: Detailed string with renderer information.
        :rtype: str
        """
        return f'Forge Renderer -> Name: {self.name}, ID: {self._id} Image Pool: {self.image_pool.__str__()}'

    def id(self) -> int:
        """
        Get the unique ID of the renderer.

        :return: ID of the renderer.
        :rtype: int
        """
        return self._id

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        self.image_pool.render(display)

    def update(self, delta_time: float) -> None:
        pass


@dataclasses.dataclass(slots=True)
class ObjectRenderer(Renderer):
    ...


@dataclasses.dataclass(slots=True)
class UIRenderer(Renderer):
    ...


def get_renderer_from_name(renderer_name: str) -> Renderer | ObjectRenderer | UIRenderer:
    """
    Retrieve a particular renderer from the renderer dictionary using the renderer name.

    :param renderer_name: Name of the renderer to be retrieved.
    :type renderer_name: str

    :return: Renderer stored in the renderer dictionary.
    :rtype: Renderer | ObjectRenderer | UIRenderer

    :raises KeyError: A renderer must be registered if it is to be retrieved.
    """
    if renderer_name not in RENDERER_IDS:
        raise KeyError(
            f'Renderer named: {renderer_name} has not been registered as a renderer and cannot be retrieved.'
        )

    return _RENDERERS[RENDERER_IDS[renderer_name]]


def get_renderer_from_id(renderer_id: int) -> Renderer | ObjectRenderer | UIRenderer:
    """
    Retrieve a registered renderer from the renderer dictionary using the renderer ID.

    :param renderer_id: ID of the renderer to be retrieved.
    :type renderer_id: int

    :return: Renderer stored in the renderer dictionary.
    :rtype: Renderer | ObjectRenderer | UIRenderer
    """
    if renderer_id not in _RENDERERS:
        raise KeyError(
            f'Renderer with ID: {renderer_id} has not been registered as a renderer and cannot be retrieved.'
        )

    return _RENDERERS[renderer_id]


# A no-inspection is used because all overloaded functions will be re-written from scratch.
# noinspection DuplicatedCode
def delete_renderer_from_name(renderer_name: str) -> None:
    """
    Delete a registered renderer from the renderer dictionary using the renderer name and free the ID of the renderer.

    :param renderer_name: Name of the renderer to be deleted.
    :type renderer_name: str

    :raises KeyError: A renderer must be registered if it is to be deleted.
    """
    if renderer_name not in RENDERER_IDS:
        raise KeyError(f'Renderer named: {renderer_name} has not been registered as a renderer and cannot be deleted.')

    _RENDERERS.pop(RENDERER_IDS[renderer_name])
    forge.core.utils.id.delete_id(RENDERER_IDS[renderer_name])
    RENDERER_IDS.pop(renderer_name)


def delete_renderer_from_id(renderer_id: int) -> None:
    """
    Delete a registered renderer from the renderer dictionary using the renderer ID and free the ID of the renderer.

    :param renderer_id: ID of the renderer to be deleted.
    :type renderer_id: int

    :raises KeyError: A renderer must be registered if it is to be deleted.
    """
    if renderer_id not in _RENDERERS:
        raise KeyError(f'Renderer with ID: {renderer_id} has not been registered as a renderer and cannot be deleted.')

    renderer_name = _RENDERERS.pop(renderer_id).name
    forge.core.utils.id.delete_id(renderer_id)
    RENDERER_IDS.pop(renderer_name)
