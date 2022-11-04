"""
Sliders in Hearth.
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
import forge.core.utils.math
import forge.hearth.components.base
import forge.hearth.elements.base
import forge.hearth.elements.shapes
import forge.hearth.elements.text
import forge.hearth.settings
import forge.hearth.utils.bounds


class Slider(forge.hearth.components.base.UIComponent):
    """
    Base slider class for Hearth.
    """

    __slots__ = 'start_value', 'end_value', 'move_function', 'move_event', 'bar', 'grabber', '_id'

    def __init__(
            self,
            start_value: int | float, end_value: int | float,
            move_function: typing.Callable[[], None] | None,
            move_event: forge.core.managers.event.Event | None,
            top_left: forge.core.physics.vector.Vector2D,
            bar_width: int,
            bar_color: forge.core.engine.color.Color, grabber_color: forge.core.engine.color.Color,
            bar_height: int = 10, grabber_radius: int = 15,
            bar_line_width: int = 0, grabber_line_width: int = 0,
            bar_corner_radius: int | None = None,
            bar_border: forge.hearth.elements.shapes.Border | None = None,
            grabber_border: forge.hearth.elements.shapes.Border | None = None,
    ) -> None:
        """
        Initialize the slider.

        :param start_value: Start value of the slider.
        :type start_value: int | float
        :param end_value: End value of ths slider.
        :type end_value: int | float
        :param move_function: Function to call when the slider is moved.
        :type move_function: typing.Callable[[]. None] | None
        :param move_event: Event to post when the slider is moved.
        :param top_left: forge.core.managers.event.Event | None
        :param bar_width: Width of the slider bar.
        :type bar_width: int
        :param bar_color: Color of the slider bar.
        :type bar_color: forge.core.engine.color.Color
        :param grabber_color: Color of the slider grabber.
        :type grabber_color: forge.core.engine.color.Color
        :param bar_height: Height of the slider bar; defaults to 10.
        :type bar_height: int
        :param grabber_radius: Radius of the slider grabber; defaults to 15.
        :type grabber_radius: int
        :param bar_line_width: Width of the line of the slider bar; defaults to 0.
        :type bar_line_width: int
        :param grabber_line_width: Width of the slider grabber; defaults to 0.
        :type grabber_line_width: int
        :param bar_corner_radius: Radius of the corner of the slider bar; defaults to None.
        :type bar_corner_radius: int | None
        :param bar_border: Border of the slider bar; defaults to None.
        :type bar_border: forge.hearth.elements.shapes.Border | None
        :param grabber_border: Border of the slider grabber; defaults to None.
        :type grabber_border: forge.hearth.elements.shapes.Border | None
        """
        if end_value <= start_value:
            raise ValueError('The minimum value cannot be greater than the maximum value.')

        self.start_value = start_value
        self.end_value = end_value
        self.move_function = move_function
        self.move_event = move_event

        self.bar = forge.hearth.elements.shapes.Rectangle(
            top_left, bar_width, bar_height, bar_color,
            line_width=bar_line_width, corner_radius=bar_corner_radius, border=bar_border
        )

        self.grabber = forge.hearth.elements.shapes.Circle(
            forge.core.physics.vector.Vector2D(top_left.x, top_left.y + bar_height // 2), grabber_radius, grabber_color,
            line_width=grabber_line_width, border=grabber_border
        )

        self._id = forge.core.utils.id.generate_random_id()

    def __repr__(self) -> str:
        """
        Internal representation of the slider.

        :return: Simple string with slider data.
        :rtype: str
        """
        return f'Slider -> Value: {self.value()}, ' \
               f'On Move Function: {self.move_function.__name__ if self.move_function else None}, ' \
               f'On Move Event: ({self.move_event.__repr__() if self.move_event else None})'

    def __str__(self) -> str:
        """
        String representation of the slider.

        :return: Detailed string with slider data.
        :rtype: str
        """
        return f'Forge Slider -> Value: {self.value()}, Clamped Value -> {self.value_clamped()}, ' \
               f'On Move Function: {self.move_function.__name__ if self.move_function else None}, ' \
               f'On Move Event: ({self.move_event.__str__() if self.move_event else None}), ' \
               f'Bar -> ({self.bar.__str__()}), Grabber: ({self.grabber.__str__()})'

    def value(self) -> float:
        """
        Compute the current raw value of the slider.

        :return: Raw value of the slider.
        :rtype: float
        """
        return (self.grabber.center.x - self.bar.top_left.x) * (self.end_value - self.start_value) / self.bar.width

    def value_clamped(self) -> float:
        """
        Compute the current clamped value of the slider.

        :return: Clamped value of the slider.
        :rtype: float
        """
        return (self.grabber.center.x - self.bar.top_left.x) / self.bar.width

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        """
        Add the slider and its text to their renderers respectively.

        :param component_renderer_name: Name of the renderer to which the slider is to be added; defaults to the base
                                        component renderer.
        :type component_renderer_name: str
        :param ui_renderer_name: Name of the renderer to which the elements of the slider are to be added; defaults to
                                 the base UI renderer.
        :type ui_renderer_name: str
        """
        forge.core.engine.renderer.get_renderer_from_name(component_renderer_name).components.append(self)
        self.bar.add_to_renderer(ui_renderer_name)
        self.grabber.add_to_renderer(ui_renderer_name)

    def is_moved(self) -> bool:
        """
        Check whether the slider is moved or not.

        :return: True if the slider is moved; else False.
        :rtype: bool
        """
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_pressed(forge.core.managers.mouse.MouseButton.LEFT):
            if forge.hearth.utils.bounds.point_within_rectangle(
                    mouse_position,
                    forge.core.physics.vector.Vector2D(
                        self.bar.top_left.x - forge.hearth.settings.PADDING,
                        self.bar.top_left.y - self.grabber.radius
                    ),
                    self.bar.width + forge.hearth.settings.PADDING, self.grabber.radius * 2
            ):
                return True

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        """
        Render the slider and its elements to the display.

        :param display: Display to which the slider and its elements are to be rendered.
        :type display: forge.core.utils.aliases.Surface
        """
        self.bar.render(display)
        self.grabber.render(display)

    def update(self) -> None:
        """
        Update the slider.
        """
        if self.is_moved():
            self.grabber.center.x = forge.core.managers.mouse.position().x
            self.grabber.center.x = forge.core.utils.math.clamp(
                self.grabber.center.x, self.bar.top_left.x, self.bar.top_left.x + self.bar.width
            )

            if self.move_function is not None:
                self.move_function()

            if self.move_event is not None:
                self.move_event.post()
