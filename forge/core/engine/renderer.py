"""
Renderers for Forge.
"""
from __future__ import annotations

import dataclasses
import typing

import attrs

import forge.core.engine.image
import forge.core.utils.aliases
import forge.core.utils.id
import forge.hearth.settings

if typing.TYPE_CHECKING:
    import forge.hearth.elements.base
    import forge.hearth.components.base

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

        :return: Simple string with renderer data.
        :rtype: str
        """
        return f'Renderer -> Name: {self.name}, Image Count: {len(self.image_pool.images())}'

    def __str__(self) -> str:
        """
        String representation of the renderer.

        :return: Detailed string with renderer data.
        :rtype: str
        """
        return f'Forge Renderer -> Name: {self.name}, Image Pool: ({self.image_pool.__str__()})'

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


@dataclasses.dataclass
class ObjectRenderer(Renderer):
    def __repr__(self) -> str:
        """
        Internal representation of the object renderer.

        :return: Simple string with object renderer data.
        :rtype: str
        """
        return f'Object Renderer -> Name: {self.name}, Image Count: {len(self.image_pool.images())}'

    def __str__(self) -> str:
        """
        String representation of the object renderer.

        :return: Detailed string with object renderer data.
        :rtype: str
        """
        return f'Forge Object Renderer -> Name: {self.name}, Image Pool: ({self.image_pool.__str__()})'


@dataclasses.dataclass
class UIRenderer(Renderer):
    elements: list['forge.hearth.elements.base.UIElement'] = dataclasses.field(default_factory=list)

    def __repr__(self) -> str:
        """
        Internal representation of the ui renderer.

        :return: Simple string with ui renderer data.
        :rtype: str
        """
        return f'UI Renderer -> Name: {self.name}, Image Count: {len(self.image_pool.images())}, ' \
               f'Element Count: {len(self.elements)}'

    def __str__(self) -> str:
        """
        String representation of the ui renderer.

        :return: Detailed string with ui renderer data.
        :rtype: str
        """
        return f'Forge UI Renderer -> Name: {self.name}, Image Pool: ({self.image_pool.__str__()}), ' \
               f'Elements: {self.elements}'

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        super().render(display)

        rendered_element_ids: set[int] = set()

        for element in self.elements:
            if element.id() in rendered_element_ids:
                continue

            element.render(display)
            rendered_element_ids.add(element.id())

            if forge.hearth.settings.AUTO_RENDER_CHILDREN:
                for child in element.children:
                    rendered_element_ids.add(child.id())

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        updated_element_ids: set[int] = set()

        for element in self.elements:
            if element.id() in updated_element_ids:
                continue

            element.update()
            updated_element_ids.add(element.id())

            if forge.hearth.settings.AUTO_UPDATE_CHILDREN:
                for child in element.children:
                    updated_element_ids.add(child.id())


@dataclasses.dataclass
class ComponentRenderer(Renderer):
    components: list['forge.hearth.components.base.UIComponent'] = dataclasses.field(default_factory=list)

    def __repr__(self) -> str:
        """
        Internal representation of the component renderer.

        :return: Simple string with component renderer data.
        :rtype: str
        """
        return f'Component Renderer -> Name: {self.name}, Image Count: {len(self.image_pool.images())}, ' \
               f'Component Count: {len(self.components)}'

    def __str__(self) -> str:
        """
        String representation of the component renderer.

        :return: Detailed string with component renderer data.
        :rtype: str
        """
        return f'Forge Component Renderer -> Name: {self.name}, Image Pool: ({self.image_pool.__str__()}), ' \
               f'Components: {self.components}'

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        super().render(display)

        for component in self.components:
            component.render(display)

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        for component in self.components:
            component.update()


def get_renderer_from_name(renderer_name: str) -> Renderer | ObjectRenderer | UIRenderer | ComponentRenderer:
    """
    Retrieve a particular renderer from the renderer dictionary using the renderer name.

    :param renderer_name: Name of the renderer to be retrieved.
    :type renderer_name: str

    :return: Renderer stored in the renderer dictionary.
    :rtype: Renderer | ObjectRenderer | UIRenderer | ComponentRenderer

    :raises KeyError: A renderer must be registered if it is to be retrieved.
    """
    if renderer_name not in RENDERER_IDS:
        raise KeyError(
            f'Renderer named: {renderer_name} has not been registered as a renderer and cannot be retrieved.'
        )

    return _RENDERERS[RENDERER_IDS[renderer_name]]


def get_renderer_from_id(renderer_id: int) -> Renderer | ObjectRenderer | UIRenderer | ComponentRenderer:
    """
    Retrieve a registered renderer from the renderer dictionary using the renderer ID.

    :param renderer_id: ID of the renderer to be retrieved.
    :type renderer_id: int

    :return: Renderer stored in the renderer dictionary.
    :rtype: Renderer | ObjectRenderer | UIRenderer | ComponentRenderer
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
