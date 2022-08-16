"""
Renderers for Forge.
"""
from __future__ import annotations

import typing

import core.engine.image
import core.utils.aliases
import core.utils.base

if typing.TYPE_CHECKING:
    import core.physics.rigid_body
    import core.physics.static_body
    import core.physics.line

_RENDERERS: dict[str, Renderer] = {}


class Renderer(core.utils.base.Renderable):
    """
    Forge's base renderer which only supports images.
    """

    __slots__ = 'name', 'image_pool'

    def __init__(self, name: str, images: list[core.engine.image.Image]) -> None:
        """
        Initialise a new renderer and check whether the supplied renderer name is unique and not taken by another
        existing renderer. If unique, add the renderer to the dictionary.

        :param name: Name of the renderer.
        :type name: str
        :param images: Images for the renderer to render.
        :type images: list[core.engine.image.Image]

        :raises ValueError: All renderer names must be unique.
        """
        self.name = name

        try:
            self.image_pool = core.engine.image.ImagePool(name, images)
            _RENDERERS[name] = self

        except ValueError:
            raise ValueError(f'Cannot create two renderers of the same name: {name}.')

    def render(self, display: core.utils.aliases.Surface) -> None:
        """
        Render all the images from the pool to the display.

        :param display: Display to which the images are to be rendered.
        :type display: core.utils.aliases.Surface
        """
        for image in self.image_pool.images():
            image.render(display)

    def update(self, delta_time: float) -> None:
        """
        Update the renderer; called every frame.

        :param delta_time: Delta time between frames.
        :type delta_time: float
        """
        pass


class ObjectRenderer(Renderer):
    """
    Forge's base object renderer to render physics based objects to the display.
    """

    __slots__ = 'static_bodies', 'rigid_bodies', 'lines'

    def __init__(
            self,
            name: str, images: list[core.engine.image.Image],
            static_bodies: list['core.physics.static_body.StaticBody2D'],
            rigid_bodies: list['core.physics.rigid_body.RigidBody2D'],
            lines: list['core.physics.line.Line']
    ) -> None:
        """
        Initialise a new object renderer and check whether the supplied renderer name is unique and not taken by another
        existing renderer. If unique, add the renderer to the dictionary.

        :param name: Name of the renderer.
        :type name: str
        :param images: Images for the renderer to render.
        :type images: list[core.engine.image.Image]
        :param static_bodies: Static bodies for the renderer to render. # TODO: Static bodies not fully implemented.
        :type static_bodies: list[core.physics.static_body.StaticBody2D]
        :param rigid_bodies: Rigid bodies for the renderer to render. # TODO: Rigid bodies not fully implemented.
        :type rigid_bodies: list[core.physics.rigid_body.RigidBody2D]
        :param lines: Lines for the renderer to render.
        :type lines: list[core.physics.line.Line]

        :raises ValueError: All renderer names must be unique.
        """
        super().__init__(name, images)

        self.static_bodies = static_bodies
        self.rigid_bodies = rigid_bodies
        self.lines = lines

    def render(self, display: core.utils.aliases.Surface) -> None:
        """
        Render all the images from the pool, static bodies, rigid bodies and lines to the display.

        :param display: Display to which the objects are to be rendered.
        :type display: core.utils.aliases.Surface
        """
        super().render(display)

        # for static_body in self.static_bodies:
        #     static_body.render()
        #
        # for rigid_body in self.rigid_bodies:
        #     rigid_body.render()
        #
        # for line in self.lines:
        #     line.render(display)


class UIRenderer(Renderer):
    """
    Forge's base UI renderer to render Hearth UI elements to the display.
    """
    ...


def get_renderer(renderer_name: str) -> Renderer | ObjectRenderer | UIRenderer:
    """
    Get a particular renderer.

    :param renderer_name: Name of the renderer to retrieve.
    :type renderer_name: str

    :return: Forge renderer, if it exists.
    :rtype: Renderer | ObjectRenderer | UIRenderer

    :raises KeyError: A renderer must be registered if it is to be retrieved.
    """
    if renderer_name not in _RENDERERS:
        raise KeyError(
            f'Renderer named: {renderer_name} has not been registered as a renderer and cannot be retrieved.'
        )

    return _RENDERERS[renderer_name]


def delete_renderer(renderer_name: str) -> None:
    """
    Delete a particular renderer.

    :param renderer_name: Name of the renderer to delete.
    :type renderer_name: str

    :raises KeyError: A renderer must be registered if it is to be deleted.
    """
    if renderer_name not in _RENDERERS:
        raise KeyError(f'Renderer named: {renderer_name} has not been registered as a renderer and cannot be deleted.')

    _RENDERERS.pop(renderer_name)
