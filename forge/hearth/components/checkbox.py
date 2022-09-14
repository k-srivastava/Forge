import enum

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
    SOLID = enum.auto()
    BORDERED = enum.auto()
    CHECKED = enum.auto()


class _Checkbox(forge.hearth.components.base.UIComponent):
    __slots__ = 'click_event', 'value', 'style', '_id'

    def __init__(
            self, click_event: forge.core.managers.event.Event, value: bool = False,
            style: CheckboxStyle = CheckboxStyle.SOLID
    ) -> None:
        self.click_event = click_event
        self.value = value
        self.style = style

        self._id = forge.core.utils.id.generate_random_id()

    def id(self) -> int:
        return self._id

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        forge.core.engine.renderer.get_renderer_from_name(component_renderer_name).components.append(self)

    def is_clicked(self) -> None:
        ...

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
        ...

    def update(self) -> None:
        if self.is_clicked():
            self.value = not self.value
            self.click_event.post()


class SquareCheckbox(_Checkbox):
    def __init__(
            self,
            top_left: forge.core.physics.vector.Vector2D, size: int,
            color: forge.core.engine.color.Color,
            click_event: forge.core.managers.event.Event,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            corner_radius: int | None = None,
            border: forge.hearth.elements.shapes.Border | None = None,
            value: bool = False,
            style: CheckboxStyle = CheckboxStyle.SOLID
    ) -> None:
        super().__init__(click_event, value, style)
        self.square = forge.hearth.elements.shapes.Rectangle(
            top_left, size, size, color, parent, line_width, corner_radius, border
        )

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        super().add_to_renderer(component_renderer_name, ui_renderer_name)
        self.square.add_to_renderer(ui_renderer_name)

    def is_clicked(self) -> bool:
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_rectangle(
                mouse_position,
                self.square.top_left, self.square.width, self.square.height
            )

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
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
        self.square.update()
        super().update()


class CircleCheckbox(_Checkbox):
    def __init__(
            self,
            center: forge.core.physics.vector.Vector2D, radius: int,
            color: forge.core.engine.color.Color,
            click_event: forge.core.managers.event.Event,
            parent: forge.hearth.elements.base.UIElement | None = None,
            line_width: int = 0,
            border: forge.hearth.elements.shapes.Border | None = None,
            value: bool = False,
            style: CheckboxStyle = CheckboxStyle.SOLID
    ) -> None:
        super().__init__(click_event, value, style)
        self.circle = forge.hearth.elements.shapes.Circle(
            center, radius, color, parent, line_width, border
        )

    def add_to_renderer(
            self,
            component_renderer_name: str = forge.core.engine.constants.DISPLAY_COMPONENT_RENDERER,
            ui_renderer_name: str = forge.core.engine.constants.DISPLAY_UI_RENDERER
    ) -> None:
        super().add_to_renderer(component_renderer_name, ui_renderer_name)
        self.circle.add_to_renderer(ui_renderer_name)

    def is_clicked(self) -> bool:
        mouse_position: forge.core.physics.vector.Vector2D = forge.core.managers.mouse.position()

        if forge.core.managers.mouse.is_clicked(forge.core.managers.mouse.MouseButton.LEFT):
            return forge.hearth.utils.bounds.point_within_circle(mouse_position, self.circle.center, self.circle.radius)

        return False

    def render(self, display: forge.core.utils.aliases.Surface) -> None:
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
        self.circle.update()
        super().update()
