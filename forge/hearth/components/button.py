"""
Buttons in Hearth.
"""
import typing

import forge.core.engine.color
import forge.core.engine.constants
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

    __slots__ = 'click_function', 'click_event', 'text', 'text_centered', '_id'

    def __init__(
            self,
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event | None,
            text: forge.hearth.elements.text.Text,
            text_centered: bool = True,
    ) -> None:
        """
        Initialize the button.

        :param click_function: Function to call when the button is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked.
        :type click_event: forge.core.managers.event.Event | None
        :param text: Text to be rendered onto the button.
        :type text: forge.hearth.elements.text.Text
        :param text_centered: Whether the button text is to be centered on the button; defaults to True.
        :type text_centered: bool
        """
        self.click_function = click_function
        self.click_event = click_event
        self.text = text
        self.text_centered = text_centered

        self._id = forge.core.utils.id.generate_random_id()

        if not text_centered:
            forge.hearth.elements.shapes.calculate_relative_positions(self, [self.text.top_left])

    def __repr__(self) -> str:
        """
        Internal representation of the button.

        :return: Simple string with button data.
        :rtype: str
        """
        return f'Button -> Text: ({self.text.__repr__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the button.

        :return: Detailed string with button data.
        :rtype: str
        """
        return f'Forge Button -> Text: ({self.text.__str__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def id(self) -> int:
        """
        Get the unique ID of the button.

        :return: ID of the button.
        :rtype: int
        """
        return self._id

    def add_to_renderer(self) -> None:
        """
        Add the button and its text to their renderers respectively.
        """
        self.text.add_to_renderer()

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
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event | None,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            corner_radius: int | None = None,
            border: forge.hearth.elements.base.Border | None = None,
            text_: str = '', font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True
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
        :param click_function: Function to call when the button is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked.
        :type click_event: forge.core.managers.event.Event | None
        :param parent: Parent of the button; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the button line; defaults to 0.
        :type line_width: int
        :param corner_radius: Radii of the corners of the button; defaults to None.
        :type corner_radius: int | None
        :param border: Border of the button; defaults to None.
        :type border: forge.hearth.elements.shapes.Border | None
        :param text_: Text to be rendered onto the button; defaults to an empty string.
        :type text_: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on the button; defaults to True.
        :type text_centered: bool
        """
        self.children = []

        self.rectangle = forge.hearth.elements.shapes.Rectangle(
            top_left, width, height, color, parent, line_width, corner_radius, border
        )

        text_ = forge.hearth.elements.text.Text(
            text_, font_size, top_left, font_face, text_color, text_background_color, self, anti_aliasing
        )

        super().__init__(click_function, click_event, text_, text_centered)

        if self.text_centered:
            _center_text(self.rectangle.center, self.text)

    def __repr__(self) -> str:
        """
        Internal representation of the rectangular button.

        :return: Simple string with rectangular button data.
        :rtype: str
        """
        return f'Rectangular Button -> Text: ({self.text.__repr__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the rectangular button.

        :return: Detailed string with rectangular button data.
        :rtype: str
        """
        return f'Forge Rectangular Button -> Text: ({self.text.__str__()}), Rectangle: ({self.rectangle.__str__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def add_to_renderer(self) -> None:
        """
        Add the button and its text to their renderers respectively.
        """
        self.rectangle.add_to_renderer()
        self.text.add_to_renderer()

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_pressed(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_rectangle(
                mouse_position,
                self.rectangle.top_left, self.rectangle.width, self.rectangle.height
            )

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the button and its text to the display.

        :param display: Display to which the UI component and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        self.rectangle.render(display)
        super().render(display)

    def update(self) -> None:
        """
        Update the button.
        """
        self.rectangle.update()
        super().update()

        if self.text is not None:
            _center_text(self.rectangle.center, self.text)


class CircularButton(Button):
    """
    Circular button class in Hearth.
    """

    __slots__ = 'circle'

    def __init__(
            self,
            center: forge.core.physics.vector.Vector2D, radius: int,
            color: forge.core.engine.color.Color,
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event | None,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: forge.hearth.elements.base.Border | None = None,
            text: str = '', font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color(255, 255, 255),
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True
    ) -> None:
        """
        Initialize the rectangular button.

        :param center: Center of the button.
        :type center: forge.core.physics.vector.Vector2D
        :param color: Color of the button.
        :type color: forge.core.engine.color.Color
        :param click_function: Function to call when the button is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked.
        :type click_event: forge.core.managers.event.Event
        :param parent: Parent of the button; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the button line; defaults to 0.
        :type line_width: int
        :param border: Border of the button; defaults to None.
        :type border: forge.hearth.elements.shapes.Border | None
        :param text: Text to be rendered onto the button; defaults to an empty string.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on the button; defaults to True.
        :type text_centered: bool
        """
        self.children = []

        self.circle = forge.hearth.elements.shapes.Circle(center, radius, color, parent, line_width, border)

        text = forge.hearth.elements.text.Text(
            text, font_size, self.circle.top_left, font_face, text_color, text_background_color, self, anti_aliasing
        )

        super().__init__(click_function, click_event, text, text_centered)

        if self.text_centered:
            _center_text(self.circle.center, self.text)

    def __repr__(self) -> str:
        """
        Internal representation of the circular button.

        :return: Simple string with circular button data.
        :rtype: str
        """
        return f'Circular Button -> Text: ({self.text.__repr__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the circular button.

        :return: Detailed string with circular button data.
        :rtype: str
        """
        return f'Forge Circular Button -> Text: ({self.text.__str__()}), Circle: ({self.circle.__str__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def add_to_renderer(self) -> None:
        """
       Add the button and its text to their renderers respectively.
       """
        self.circle.add_to_renderer()
        self.text.add_to_renderer()

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_pressed(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_circle(mouse_position, self.circle.center, self.circle.radius)

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the button and its text to the display.

        :param display: Display to which the UI component and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        self.circle.render(display)
        super().render(display)

    def update(self) -> None:
        """
        Update the button.
        """
        self.circle.update()
        super().update()

        if self.text is not None:
            _center_text(self.circle.center, self.text)


class PolygonalButton(Button):
    """
    Polygonal button class in Hearth.
    """

    __slots__ = 'polygon'

    def __init__(
            self,
            vertices: list[forge.core.physics.vector.Vector2D],
            color: forge.core.engine.color.Color,
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: forge.hearth.elements.base.Border | None = None,
            text: str = '', font_size: int = forge.hearth.settings.DEFAULT_FONT_SIZE,
            font_face: str = forge.hearth.settings.DEFAULT_FONT_FACE,
            text_color: forge.core.engine.color.Color = forge.core.engine.color.Color,
            text_background_color: forge.core.engine.color.Color | None = None,
            anti_aliasing: bool = True, text_centered: bool = True
    ) -> None:
        """
        Initialize the polygonal button.

        :param vertices: Vertices of the button.
        :type vertices: list[forge.core.physics.vector.Vector2D]
        :param color: Color of the button.
        :type color: forge.core.engine.color.Color
        :param click_function: Function to call when the button is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the button is clicked.
        :type click_event: forge.core.managers.event.Event
        :param parent: Parent of the button; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the button line; defaults to 0.
        :type line_width: int
        :param border: Border of the button; defaults to None.
        :type border: forge.hearth.elements.shapes.Border | None
        :param text: Text to be rendered onto the button; defaults to an empty string.
        :type text: str
        :param font_size: Font size of the text; defaults to forge.hearth.settings.DEFAULT_FONT_SIZE.
        :type font_size: int
        :param font_face: Font face of the text; defaults to forge.hearth.settings.DEFAULT_FONT_FACE.
        :param text_color: Color of the text; defaults to (R: 255, G: 255, B: 255) - white.
        :type text_color: forge.core.engine.color.Color
        :param text_background_color: Color of the bounding box of the text; defaults to None.
        :type text_background_color: forge.core.engine.color.Color | None
        :param anti_aliasing: Whether to anti-alias the text being rendered; defaults to True.
        :type anti_aliasing: bool
        :param text_centered: Whether the button text is to be centered on the button; defaults to True.
        :type text_centered: bool
        """
        self.children = []

        self.polygon = forge.hearth.elements.shapes.Polygon(vertices, color, parent, line_width, border)

        text = forge.hearth.elements.text.Text(
            text, font_size, self.polygon.top_left, font_face, text_color, text_background_color, self, anti_aliasing
        )

        super().__init__(click_function, click_event, text, text_centered)

        if self.text_centered:
            _center_text(self.polygon.center, self.text)

    def __repr__(self) -> str:
        """
        Internal representation of the polygonal button.

        :return: Simple string with polygonal button data.
        :rtype: str
        """
        return f'Polygonal Button -> Text: ({self.text.__repr__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the polygonal button.

        :return: Detailed string with polygonal button information.
        :rtype: str
        """
        return f'Forge Polygonal Button -> Text: ({self.text.__str__()}), Polygon: ({self.polygon.__str__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def add_to_renderer(self) -> None:
        """
        Add the button and its text to their renderers respectively.
        """
        self.polygon.add_to_renderer()
        self.text.add_to_renderer()

    def is_clicked(self) -> bool:
        """
        Check whether the button is clicked or not.

        :return: True if the button is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_pressed(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_polygon(mouse_position, self.polygon.vertices)

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the button and its text to the display.

        :param display: Display to which the UI component and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        self.polygon.render(display)
        super().render(display)

    def update(self) -> None:
        """
        Update the button.
        """
        self.polygon.update()
        super().update()

        if self.text is not None:
            _center_text(self.polygon.center, self.text)


def _center_text(position: forge.core.physics.vector.Vector2D, text: forge.hearth.elements.text.Text) -> None:
    """
    Center the position of a text box with respect to a specified position.

    :param position: Position with respect to which the text has to be centered.
    :type position: forge.core.physics.vector.Vector2D
    :param text: Text which has to be centered.
    :type text: forge.hearth.elements.text.Text
    """
    dimensions: forge.core.physics.vector.Vector2D = text.dimensions()

    text.top_left.x = position.x - (dimensions.x // 2)
    text.top_left.y = position.y - (dimensions.y // 2)
