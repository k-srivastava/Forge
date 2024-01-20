"""
Base renderer for Forge.
"""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from forge.core.engine.constants import CORE_RENDERER
from forge.core.engine.image import Image, ImagePool
from forge.core.utils import id
from forge.core.utils.aliases import Surface
from forge.hearth.settings import AUTO_RENDER_CHILDREN, AUTO_UPDATE_CHILDREN

if TYPE_CHECKING:
    from forge.core.engine.game_object import GameObject
    from forge.hearth.components.base import UIComponent
    from forge.hearth.elements.base import Shape, UIElement

_MASTER_RENDERER: list[Optional[MasterRenderer]] = [None]


class CoreRenderer:
    """
    Renderer for images, shapes and game objects.
    """

    def __init__(self) -> None:
        """
        Initialize the core renderer.
        """
        self.shapes: list[Shape] = []
        self.game_objects: list[GameObject] = []
        self.image_pool: ImagePool = ImagePool(
            CORE_RENDERER, _images=[], _belongs_to_renderer=True
        )
        self._id: int = id.generate_random_id()

    def id(self) -> int:
        """
        Get the unique ID of the core renderer.

        :return: ID of the core renderer.
        :rtype: int
        """
        return self._id

    def render(self, display: Surface) -> None:
        """
        Render all the images, shapes and game objects.

        :param display: Display to which the image and shapes are to be rendered.
        :type display: Surface
        """
        for shape in self.shapes:
            shape.render(display)

        for game_object in self.game_objects:
            game_object.render(display)

        self.image_pool.render(display)

    def update(self, delta_time: float) -> None:
        """
        Update all the shapes and game objects.

        :param delta_time: Delta time for the current pass.
        :type delta_time: float
        """
        for shape in self.shapes:
            shape.update()

        for game_object in self.game_objects:
            game_object.update(delta_time)


class UIRenderer:
    """
    Renderer for UI elements and components.
    """

    def __init__(self) -> None:
        """
        Initialize the UI renderer.
        """
        self.elements: list[UIElement] = []
        self.components: list[UIComponent] = []
        self._id: int = id.generate_random_id()

    def id(self) -> int:
        """
        Get the unique ID of the UI renderer.

        :return: ID of the UI renderer.
        :rtype: int
        """
        return self._id

    def render(self, display: Surface) -> None:
        """
        Render all the UI elements and components.

        :param display: Display to which the UI elements and components are to be rendered.
        :type display: Surface
        """
        rendered_element_ids: set[int] = set()

        for element in self.elements:
            element_id = element.id()

            if element_id in rendered_element_ids:
                continue

            element.render(display)
            rendered_element_ids.add(element_id)

            if AUTO_RENDER_CHILDREN:
                for child in element.children:
                    rendered_element_ids.add(child.id())

        for component in self.components:
            component.render(display)

    def update(self, delta_time: float) -> None:
        """
        Update all the UI elements and shapes.

        :param delta_time: Delta time for the current pass.
        :type delta_time: float
        """
        updated_element_ids: set[int] = set()

        for element in self.elements:
            element_id = element.id()

            if element_id in updated_element_ids:
                continue

            element.update()
            updated_element_ids.add(element_id)

            if AUTO_UPDATE_CHILDREN:
                for child in element.children:
                    updated_element_ids.add(child.id())

        for component in self.components:
            component.update()


class MasterRenderer:
    """
    Master renderer containing all base renderers.
    """

    def __init__(self) -> None:
        """
        Initialize the master renderer.
        """
        if _MASTER_RENDERER[0] is not None:
            raise SyntaxError()

        self._core_renderer: CoreRenderer = CoreRenderer()
        self._ui_renderer: UIRenderer = UIRenderer()
        self._id: int = id.generate_random_id()

        _MASTER_RENDERER[0] = self

    def id(self) -> int:
        """
        Get the unique ID of the master renderer.

        :return: ID of the master renderer.
        :rtype: int
        """
        return self._id

    def add_image(self, image: Image) -> None:
        """
        Add an image to the core renderer of the master renderer.

        :param image: Image to be added.
        :type image: Image
        """
        self._core_renderer.image_pool += image

    def add_images(self, images: list[Image]) -> None:
        """
        Add a multiple images to the core renderer of the master renderer.

        :param images: Images to be added.
        :type images: list[Image]
        """
        self._core_renderer.image_pool += images

    def remove_image(self, image: Image) -> None:
        """
        Remove an image from the core renderer of the master renderer.

        :param image: Image to be removed.
        :type image: Image
        """
        self._core_renderer.image_pool -= image

    def add_shape(self, shape: Shape) -> None:
        """
        Add a shape to the core renderer of the master renderer.

        :param shape: Shape to be added.
        :type shape: Shape
        """
        self._core_renderer.shapes.append(shape)

    def remove_shape(self, shape: Shape) -> None:
        """
        Remove a shape from the core renderer of the master renderer.

        :param shape: Shape to be removed.
        :type shape: Shape
        """
        self._core_renderer.shapes.remove(shape)

    def add_game_object(self, game_object: GameObject) -> None:
        """
        Add a game object to the core renderer of the master renderer.

        :param game_object: Game object to be added.
        :type game_object: GameObject
        """
        self._core_renderer.game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject) -> None:
        """
        Remove a game object from the core renderer of the master renderer.

        :param game_object: Game object to be removed.
        :type game_object: GameObject
        """
        self._core_renderer.game_objects.remove(game_object)

    def add_element(self, element: UIElement) -> None:
        """
        Add an element to the UI renderer of the master renderer.

        :param element: Element to be added.
        :type element: UIElement
        """
        self._ui_renderer.elements.append(element)

    def remove_element(self, element: UIElement) -> None:
        """
        Remove an element from the UI renderer of the master renderer.

        :param element: Element to be removed.
        :type element: UIElement
        """
        self._ui_renderer.elements.remove(element)

    def add_component(self, component: UIComponent) -> None:
        """
        Add a component to the UI renderer of the master renderer.

        :param component: Component to be added.
        :type component: UIComponent
        """
        self._ui_renderer.components.append(component)

    def remove_component(self, component: UIComponent) -> None:
        """
        Remove a component from the UI renderer of the master renderer.

        :param component: Component to be removed.
        :type component: UIComponent
        """
        self._ui_renderer.components.remove(component)

    def render(self, display: Surface) -> None:
        """
        Render all the renderers.

        :param display: Display to which the renderers have to render.
        :type display: Surface
        """
        self._core_renderer.render(display)
        self._ui_renderer.render(display)

    def update(self, delta_time: float) -> None:
        """
        Update all the renderers.

        :param delta_time: Delta time for the current pass.
        :type delta_time: float
        """
        self._core_renderer.update(delta_time)
        self._ui_renderer.update(delta_time)


def get_master_renderer() -> Optional[MasterRenderer]:
    """
    Retrieve the current master renderer.

    :return: Current master renderer; if it exists.
    :rtype: Optional[MasterRenderer]
    """
    return _MASTER_RENDERER[0]
