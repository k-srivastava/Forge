"""
Buttons in Hearth.
"""
import typing

import forge.core.engine.color
import forge.core.engine.renderer
import forge.core.managers.event
import forge.core.managers.mouse
import forge.core.physics.vector
import forge.core.utils.aliases
import forge.core.utils.id
import forge.hearth.components.base
import forge.hearth.elements.base
import forge.hearth.elements.shapes
import forge.hearth.elements.text
import forge.hearth.settings
import forge.hearth.utils.bounds


class Button(forge.hearth.components.base.UIComponent):
    """
    Base button class for Hearth.
    """
    __slots__ = 'click_function', 'click_event', '_id', '_text_centered'

    def __init__(
            self,
            text: str, font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True,
            click_function: typing.Callable[[], None] | None = None,
            click_event: forge.core.managers.event.Event | None = None
    ) -> None:
        """
        Initialize the button.

        :param text: Text to be rendered onto the button.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :type font_face: str
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on to button; defaults to True.
        :type text_centered: bool
        :param click_function: Function to call when the button is clicked; defaults to None.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked; defaults to None.
        :type click_event: forge.core.managers.event.Event | None
        """
        self.children = []

        self.text = forge.hearth.elements.text.Text(
            text, font_size, forge.core.physics.vector.zero(), font_face, text_color, text_background_color,
            self, anti_aliasing
        )

        self.click_function = click_function
        self.click_event = click_event

        self._id = forge.core.utils.id.generate_random_id()
        self._text_centered = text_centered

    @property
    def text_centered(self) -> bool:
        """
        Whether the button text is to be centered on to the button.

        :return: Whether the text is centred.
        :rtype: bool
        """
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        """
        Whether the button text is to be centered on to the button and reset the text position.

        :param value: Whether the text is centred.
        :type value: bool
        """
        self._text_centered = value

    def id(self) -> int:
        """
        Get the unique ID of the button.

        :return: ID of the button.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self) -> None:
        """
        Add the button and its text to the renderer.
        """
        forge.core.engine.renderer.get_master_renderer().add_component(self)

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the button and its text to the display.

        :param display: Display to which the button and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        self.text.render(display)

    def update(self) -> None:
        """
        Update the button.
        """
        if self.is_clicked():
            if self.click_function is not None:
                self.click_function()

            if self.click_event is not None:
                self.click_event.post()

        self.text.update()


class RectangularButton(Button):
    """
    Rectangular button class in Hearth.
    """
    __slots__ = 'rectangle'

    def __init__(
            self,
            top_left: forge.core.physics.vector.Vector2D, width: int, height: int,
            color: forge.core.engine.color.Color,
            text: str, font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True,
            click_function: typing.Callable[[], None] | None = None,
            click_event: forge.core.managers.event.Event | None = None,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            corner_radius: int | None = None,
            border: forge.hearth.elements.base.Border | None = None
    ) -> None:
        """
        Initialize the rectangular button.

        :param top_left: Top-left vertex position of the button.
        :type top_left: forge.core.physics.vector.Vector2D
        :param width: Width of the button.
        :type width: int
        :param height: Height of the button.
        :type height: int
        :param color: Color of the button.
        :type color: forge.core.engine.color.Color
        :param text: Text to be rendered onto the button.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :type font_face: str
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on to button; defaults to True.
        :type text_centered: bool
        :param click_function: Function to call when the button is clicked; defaults to None.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked; defaults to None.
        :type click_event: forge.core.managers.event.Event | None
        :param parent: Parent of the button; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the button line; defaults to 0.
        :type line_width: int
        :param corner_radius: Radii of the corners of the button; defaults to None.
        :type corner_radius: int | None
        :param border: Border of the button; defaults to None.
        :type border: forge.hearth.elements.shapes.Border | None
        """
        super().__init__(
            text, font_size, font_face, text_color, text_background_color, anti_aliasing, text_centered,
            click_function, click_event
        )

        self.rectangle = forge.hearth.elements.shapes.Rectangle(
            top_left, width, height, color, parent, line_width, corner_radius, border
        )

        self.text_centered = text_centered

    @property
    def text_centered(self) -> bool:
        """
        Whether the button text is to be centered on to the button.

        :return: Whether the text is centred.
        :rtype: bool
        """
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        """
        Whether the button text is to be centered on to the button and reset the text position.

        :param value: Whether the text is centred.
        :type value: bool
        """
        self._text_centered = value

        if value:
            self.text.center = self.rectangle.center

        else:
            self.text.top_left = self.rectangle.top_left

    def add_to_renderer(self) -> None:
        """
        Add the button, its text and the rectangle to the renderer.
        """
        super().add_to_renderer()
        self.rectangle.add_to_renderer()

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_rectangle(
                mouse_position,
                self.rectangle.top_left, self.rectangle.width, self.rectangle.height
            )

        return False


class CircularButton(Button):
    """
    Circular button class in Hearth.
    """
    __slots__ = 'circle'

    def __init__(
            self,
            center: forge.core.physics.vector.Vector2D, radius: int,
            color: forge.core.engine.color.Color,
            text: str, font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True,
            click_function: typing.Callable[[], None] | None = None,
            click_event: forge.core.managers.event.Event | None = None,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
    ) -> None:
        """
        Initialize the circular button.

        :param center: Center of the button.
        :type center: forge.core.physics.vector.Vector2D
        :param radius: Radius of the button.
        :type radius: int
        :param color: Color of the button.
        :type color: forge.core.engine.color.Color
        :param text: Text to be rendered onto the button.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :type font_face: str
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on to button; defaults to True.
        :type text_centered: bool
        :param click_function: Function to call when the button is clicked; defaults to None.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked; defaults to None.
        :type click_event: forge.core.managers.event.Event | None
        :param parent: Parent of the button; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the button line; defaults to 0.
        :type line_width: int
        """
        super().__init__(
            text, font_size, font_face, text_color, text_background_color, anti_aliasing, text_centered,
            click_function, click_event
        )

        self.circle = forge.hearth.elements.shapes.Circle(center, radius, color, parent, line_width)

        self.text_centered = text_centered

    @property
    def text_centered(self) -> bool:
        """
        Whether the button text is to be centered on to the button.

        :return: Whether the text is centred.
        :rtype: bool
        """
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        """
        Whether the button text is to be centered on to the button and reset the text position.

        :param value: Whether the text is centred.
        :type value: bool
        """
        self._text_centered = value

        if value:
            self.text.center = self.circle.center

        else:
            self.text.top_left = self.circle.top_left

    def add_to_renderer(self) -> None:
        """
       Add the button, its text and the circle to the renderer.
       """
        super().add_to_renderer()
        self.circle.add_to_renderer()

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_circle(
                mouse_position,
                self.circle.center, self.circle.radius
            )

        return False


class PolygonalButton(Button):
    """
    Polygonal button class in Hearth.
    """
    __slots__ = 'polygon'

    def __init__(
            self,
            vertices: list[forge.core.physics.vector.Vector2D],
            color: forge.core.engine.color.Color,
            text: str, font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True,
            click_function: typing.Callable[[], None] | None = None,
            click_event: forge.core.managers.event.Event | None = None,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: forge.hearth.elements.base.Border | None = None
    ) -> None:
        """
        Initialize the polygonal button.

        :param vertices: Vertices of the button.
        :type vertices: list[forge.core.physics.vector.Vector2D]
        :param color: Color of the button
        :type color: forge.core.engine.color.Color
        :param text: Text to be rendered onto the button.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :type font_face: str
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on to button; defaults to True.
        :type text_centered: bool
        :param click_function: Function to call when the button is clicked; defaults to None.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked; defaults to None.
        :type click_event: forge.core.managers.event.Event | None
        :param parent: Parent of the button; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the button line; defaults to 0.
        :type line_width: int
        :param border: Border of the button; defaults to None.
        :type border: forge.hearth.elements.shapes.Border | None
        """
        super().__init__(
            text, font_size, font_face, text_color, text_background_color, anti_aliasing, text_centered,
            click_function, click_event
        )

        self.polygon = forge.hearth.elements.shapes.Polygon(
            vertices, color, parent, line_width, border
        )

        self.text_centered = text_centered

    @property
    def text_centered(self) -> bool:
        """
        Whether the button text is to be centered on to the button.

        :return: Whether the text is centred.
        :rtype: bool
        """
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        """
        Whether the button text is to be centered on to the button and reset the text position.

        :param value: Whether the text is centred.
        :type value: bool
        """
        self._text_centered = value

        if value:
            self.text.center = self.polygon.center

        else:
            self.text.top_left = self.polygon.top_left

    def add_to_renderer(self) -> None:
        """
        Add the button, its text and the polygon to the renderer.
        """
        super().add_to_renderer()
        self.polygon.add_to_renderer()

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_polygon(mouse_position, self.polygon.vertices)

        return False
