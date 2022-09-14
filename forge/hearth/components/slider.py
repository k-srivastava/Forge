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
    __slots__ = 'start_value', 'end_value', 'move_event', 'bar', 'grabber', '_id'

    def __init__(
            self,
            start_value: int | float, end_value: int | float,
            move_event: forge.core.managers.event.Event,
            top_left: forge.core.physics.vector.Vector2D,
            bar_width: int,
            bar_color: forge.core.engine.color.Color, grabber_color: forge.core.engine.color.Color,
            bar_height: int = 10, grabber_radius: int = 15,
            bar_line_width: int = 0, grabber_line_width: int = 0,
            bar_corner_radius: int | None = None,
            bar_border: forge.hearth.elements.shapes.Border | None = None,
            grabber_border: forge.hearth.elements.shapes.Border | None = None,
    ) -> None:
        if end_value <= start_value:
            raise ValueError('The minimum value cannot be greater than the maximum value.')

        self.start_value = start_value
        self.end_value = end_value
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

    def value(self) -> float:
        return (self.grabber.center.x - self.bar.top_left.x) * (self.end_value - self.start_value) / self.bar.width

    def value_clamped(self) -> float:
        return (self.grabber.center.x - self.bar.top_left.x) / self.bar.width

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        forge.core.engine.renderer.get_renderer_from_name(component_renderer_name).components.append(self)
        self.bar.add_to_renderer(ui_renderer_name)
        self.grabber.add_to_renderer(ui_renderer_name)

    def is_moved(self) -> bool:
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
        self.bar.render(display)
        self.grabber.render(display)

    def update(self) -> None:
        if self.is_moved():
            self.grabber.center.x = forge.core.managers.mouse.position().x
            self.grabber.center.x = forge.core.utils.math.clamp(
                self.grabber.center.x, self.bar.top_left.x, self.bar.top_left.x + self.bar.width
            )
            self.move_event.post()
