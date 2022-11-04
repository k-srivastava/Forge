"""
Checkboxes in Hearth.
"""
import enum
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


# A no-inspection has to be inserted because of a PyCharm bug.
# PyCharm displays erroneous warnings when using enum.auto().
# noinspection PyArgumentList
class CheckboxStyle(enum.Enum):
    """
    Enumeration of all valid checkbox check styles in Hearth.
    """
    SOLID = enum.auto()
    BORDERED = enum.auto()
    CHECKED = enum.auto()


class Checkbox(forge.hearth.components.base.UIComponent):
    """
    Base checkbox class in Hearth.
    """

    __slots__ = 'click_function', 'click_event', 'value', 'style', '_id'

    def __init__(
            self,
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event | None,
            value: bool = False, style: CheckboxStyle = CheckboxStyle.SOLID
    ) -> None:
        """
        Initialize the checkbox.

        :param click_function: Function to call when the checkbox is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the checkbox is clicked.
        :type click_event: forge.core.managers.event.Event | None
        :param value: Current checked value of the checkbox; defaults to False.
        :type value: bool
        :param style: Style of the checkbox; defaults to a solid fill style.
        :type style: CheckboxStyle
        """
        self.click_function = click_function
        self.click_event = click_event
        self.value = value
        self.style = style

        self._id = forge.core.utils.id.generate_random_id()

    def __repr__(self) -> str:
        """
        Internal representation of the checkbox.

        :return: Simple string with checkbox data.
        :rtype: str
        """
        return f'Checkbox -> Value: {self.value}, ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the checkbox.

        :return: Detailed string with checkbox data.
        :rtype: str
        """
        return f'Forge Checkbox -> Value: {self.value}, ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def id(self) -> int:
        """
        Get the unique ID of the checkbox.

        :return: ID of the checkbox.
        :rtype: int
        """
        return self._id

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        """
        Add the checkbox and its text to their renderers respectively.

        :param component_renderer_name: Name of the renderer to which the checkbox is to be added; defaults to the base
                                        component renderer.
        :type component_renderer_name: str
        :param ui_renderer_name: Name of the renderer to which the elements of the checkbox are to be added; defaults to
                                 the base UI renderer.
        :type ui_renderer_name: str
        """
        forge.core.engine.renderer.get_renderer_from_name(component_renderer_name).components.append(self)

    def is_clicked(self) -> bool:
        """
        Check if the checkbox is clicked or not.

        :return: True if the checkbox is clicked; else False.
        :rtype: bool
        """

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the checkbox and its elements to the display.

        :param display: Display to which the checkbox and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """

    def update(self) -> None:
        """
        Update the checkbox.
        """
        if self.is_clicked():
            self.value = not self.value

            if self.click_function is not None:
                self.click_function()

            if self.click_event is not None:
                self.click_event.post()


class SquareCheckbox(Checkbox):
    """
    Square checkbox class in Hearth.
    """

    __slots__ = 'square'

    def __init__(
            self,
            top_left: forge.core.physics.vector.Vector2D, size: int,
            color: forge.core.engine.color.Color,
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            corner_radius: int | None = None,
            border: forge.hearth.elements.shapes.Border | None = None,
            value: bool = False,
            style: CheckboxStyle = CheckboxStyle.SOLID
    ) -> None:
        """
        Initialize the square checkbox.

        :param top_left: Top-left vertex position of the checkbox.
        :type top_left: forge.core.physics.vector.Vector2D
        :param size: Size of the sides of the square of the checkbox.
        :type size: int
        :param color: Color of the checkbox.
        :type color: forge.core.engine.color.Color
        :param click_function: Function to call when the checkbox is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the checkbox is clicked.
        :type click_event: forge.core.managers.event.Event | None
        :param parent: Parent of the checkbox; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the checkbox line; defaults to 0.
        :type line_width: int
        :param corner_radius: Radii of the corners of the checkbox; defaults to None.
        :type corner_radius: int | None
        :param border: Border of the checkbox; defaults to None.
        :type border:  forge.hearth.elements.shapes.Border | None
        :param value: Current checked value of the checkbox; defaults to False.
        :type value: bool
        :param style: Style of the checkbox; defaults to a solid fill style.
        :type style: CheckboxStyle
        """
        super().__init__(click_function, click_event, value, style)

        self.children = []

        self.square = forge.hearth.elements.shapes.Rectangle(
            top_left, size, size, color, parent, line_width, corner_radius, border
        )

    def __repr__(self) -> str:
        """
        Internal representation of the square checkbox.

        :return: Simple string with square checkbox data.
        :rtype: str
        """
        return f'Square Checkbox -> Value: {self.value}, ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the square checkbox.

        :return: Detailed string with square checkbox data.
        :rtype: str
        """
        return f'Forge Square Checkbox -> Value: {self.value}, Square: ({self.square.__str__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        """
        Add the checkbox and its text to their renderers respectively.

        :param component_renderer_name: Name of the renderer to which the checkbox is to be added; defaults to the base
                                        component renderer.
        :type component_renderer_name: str
        :param ui_renderer_name: Name of the renderer to which the elements of the checkbox are to be added; defaults to
                                 the base UI renderer.
        :type ui_renderer_name: str
        """
        super().add_to_renderer(component_renderer_name, ui_renderer_name)
        self.square.add_to_renderer(ui_renderer_name)

    def is_clicked(self) -> bool:
        """
        Check if the checkbox is clicked or not.

        :return: True if the checkbox is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_rectangle(
                mouse_position,
                self.square.top_left, self.square.width, self.square.height
            )

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the checkbox and its elements to the display.

        :param display: Display to which the checkbox and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        if self.value:
            match self.style:
                case CheckboxStyle.SOLID:
                    self.square.line_width = 0

                case CheckboxStyle.BORDERED:
                    sub_square = forge.hearth.elements.shapes.Rectangle(
                        self.square.top_left + forge.core.physics.vector.Vector2D(8, 8),
                        self.square.width - 16, self.square.height - 16,
                        self.square.color, corner_radius=self.square.corner_radius, border=self.square.border
                    )
                    sub_square.render(display)

                case CheckboxStyle.CHECKED:
                    start_point = forge.core.physics.vector.Vector2D(
                        self.square.top_left.x + forge.hearth.settings.PADDING,
                        self.square.top_left.y + (self.square.height * 0.75) - forge.hearth.settings.PADDING
                    )

                    mid_point = forge.core.physics.vector.Vector2D(
                        self.square.top_left.x + (self.square.width * 0.25) + forge.hearth.settings.PADDING,
                        self.square.top_left.y + self.square.height - forge.hearth.settings.PADDING
                    )

                    end_point = forge.core.physics.vector.Vector2D(
                        self.square.top_left.x + (self.square.width * 0.75) + forge.hearth.settings.PADDING,
                        self.square.top_left.y + forge.hearth.settings.PADDING
                    )

                    tick_1 = forge.hearth.elements.shapes.Line(start_point, mid_point, self.square.color, line_width=3)
                    tick_2 = forge.hearth.elements.shapes.Line(mid_point, end_point, self.square.color, line_width=3)

                    tick_1.render(display)
                    tick_2.render(display)

        else:
            self.square.line_width = 3

        self.square.render(display)
        super().render(display)

    def update(self) -> None:
        """
        Update the checkbox.
        """
        self.square.update()
        super().update()


class CircularCheckbox(Checkbox):
    """
    Circular checkbox class in Hearth.
    """

    __slots__ = 'circle'

    def __init__(
            self,
            center: forge.core.physics.vector.Vector2D, radius: int,
            color: forge.core.engine.color.Color,
            click_function: typing.Callable[[], None] | None,
            click_event: forge.core.managers.event.Event,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: forge.hearth.elements.shapes.Border | None = None,
            value: bool = False,
            style: CheckboxStyle = CheckboxStyle.SOLID
    ) -> None:
        """
        Initialize the circle checkbox.

        :param center: Center of the checkbox.
        :type center: forge.core.physics.vector.Vector2D
        :param radius: Radius of the checkbox.
        :type radius: int
        :param color: Color of the checkbox.
        :type color: forge.core.engine.color.Color
        :param click_function: Function to call when the checkbox is clicked.
        :type click_function: typing.Callable[[], None] | None
        :param click_event: Event to post when the checkbox is clicked.
        :type click_event: forge.core.managers.event.Event | None
        :param parent: Parent of the checkbox; defaults to None.
        :type parent: forge.hearth.elements.base.UIElement | None
        :param line_width: Width of the checkbox line; defaults to 0.
        :type line_width: int
        :param border: Border of the checkbox; defaults to None.
        :type border:  forge.hearth.elements.shapes.Border | None
        :param value: Current checked value of the checkbox; defaults to False.
        :type value: bool
        :param style: Style of the checkbox; defaults to a solid fill style.
        :type style: CheckboxStyle
        """
        super().__init__(click_function, click_event, value, style)

        self.children = []

        self.circle = forge.hearth.elements.shapes.Circle(
            center, radius, color, parent, line_width, border
        )

    def __repr__(self) -> str:
        """
        Internal representation of the circular checkbox.

        :return: Simple string with circular checkbox data.
        :rtype: str
        """
        return f'Circular Checkbox -> Value: {self.value}, ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__repr__() if self.click_event else None})'

    def __str__(self) -> str:
        """
        String representation of the circular checkbox.

        :return: Detailed string with circular checkbox information.
        :rtype: str
        """
        return f'Forge Circular Checkbox -> Value: {self.value}, Circle: ({self.circle.__str__()}), ' \
               f'On Click Function: {self.click_function.__name__ if self.click_function else None}, ' \
               f'On Click Event: ({self.click_event.__str__() if self.click_event else None})'

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        """
        Add the checkbox and its text to their renderers respectively.

        :param component_renderer_name: Name of the renderer to which the checkbox is to be added; defaults to the base
                                        component renderer.
        :type component_renderer_name: str
        :param ui_renderer_name: Name of the renderer to which the elements of the checkbox are to be added; defaults to
                                 the base UI renderer.
        :type ui_renderer_name: str
        """
        super().add_to_renderer(component_renderer_name, ui_renderer_name)
        self.circle.add_to_renderer(ui_renderer_name)

    def is_clicked(self) -> bool:
        """
        Check if the checkbox is clicked or not.

        :return: True if the checkbox is clicked; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_circle(mouse_position, self.circle.center, self.circle.radius)

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the checkbox and its elements to the display.

        :param display: Display to which the checkbox and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        if self.value:
            match self.style:
                case CheckboxStyle.SOLID:
                    self.circle.line_width = 0

                case CheckboxStyle.BORDERED:
                    sub_circle = forge.hearth.elements.shapes.Circle(
                        self.circle.center, self.circle.radius - 8, self.circle.color, border=self.circle.border
                    )

                    sub_circle.render(display)

                case CheckboxStyle.CHECKED:
                    start_point = forge.core.physics.vector.Vector2D(
                        self.circle.center.x - self.circle.radius + (forge.hearth.settings.PADDING * 2),
                        self.circle.center.y + (self.circle.radius // 2)
                    )

                    mid_point = forge.core.physics.vector.Vector2D(
                        self.circle.center.x - forge.hearth.settings.PADDING,
                        self.circle.center.y + self.circle.radius - forge.hearth.settings.PADDING
                    )

                    end_point = forge.core.physics.vector.Vector2D(
                        self.circle.center.x + self.circle.radius - (forge.hearth.settings.PADDING * 2),
                        self.circle.center.y - (self.circle.radius // 2)
                    )

                    tick_1 = forge.hearth.elements.shapes.Line(start_point, mid_point, self.circle.color, line_width=3)
                    tick_2 = forge.hearth.elements.shapes.Line(mid_point, end_point, self.circle.color, line_width=3)

                    tick_1.render(display)
                    tick_2.render(display)

        else:
            self.circle.line_width = 3

        self.circle.render(display)
        super().render(display)

    def update(self) -> None:
        """
        Update the checkbox.
        """
        self.circle.update()
        super().update()
