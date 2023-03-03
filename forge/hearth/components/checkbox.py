"""Checkboxes in Hearth."""
from abc import abstractmethod
from enum import IntEnum, auto
from typing import Callable, Optional

from forge.core.engine.color import Color
from forge.core.managers import mouse
from forge.core.managers.event import Event
from forge.core.managers.mouse import MouseButton
from forge.core.physics.vector import Vector2D
from forge.core.utils.aliases import Surface
from forge.hearth.components.base import UIComponent
from forge.hearth.elements.base import Shape, UIElement
from forge.hearth.elements.border import Border
from forge.hearth.elements.shapes import Circle, Line, Polygon, Rectangle
from forge.hearth.settings import PADDING
from forge.hearth.utils import bounds


class CheckboxStyle(IntEnum):
    """Enumeration of all valid checkbox check styles in Hearth."""
    SOLID = auto()
    BORDERED = auto()
    CHECKED = auto()


class Checkbox(UIComponent):
    __slots__ = 'value', 'click_function', 'click_event', 'style'

    def __init__(self, value: bool, children: list[UIElement | Shape], style: CheckboxStyle = CheckboxStyle.SOLID,
                 click_function: Optional[Callable[[], None]] = None, click_event: Optional[Event] = None) -> None:
        super().__init__(children)

        self.value = value
        self.click_function = click_function
        self.click_event = click_event
        self.style = style

    @abstractmethod
    def is_clicked(self) -> bool:
        """"""

    def update(self) -> None:
        if self.is_clicked():
            self.value = not self.value

            if self.click_function is not None:
                self.click_function()

            if self.click_event is not None:
                self.click_event.post()

        super().update()


class SquareCheckbox(Checkbox):
    __slots__ = 'square'

    def __init__(self, top_left: Vector2D, size: int, color: Color, value: bool, children: list[UIElement | Shape],
                 line_width: int = 0, corner_radius: Optional[int] = None, border: Optional[Border] = None,
                 style: CheckboxStyle = CheckboxStyle.SOLID, click_function: Optional[Callable[[], None]] = None,
                 click_event: Optional[Event] = None) -> None:
        super().__init__(value, children, style, click_function, click_event)

        self.square = Rectangle(
            top_left, size, size, color, line_width=line_width, corner_radius=corner_radius,
            border=border
        )

    def is_clicked(self) -> bool:
        if mouse.is_clicked(MouseButton.LEFT):
            return bounds.point_within_rectangle(
                mouse.position(), self.square.top_left, self.square.width, self.square.height
            )

        return False

    def render(self, display: Surface) -> None:
        if self.value:
            match self.style:
                case CheckboxStyle.SOLID:
                    self.square.line_width = 0

                case CheckboxStyle.BORDERED:
                    sub_square = Rectangle(
                        self.square.top_left + Vector2D(PADDING // 2, PADDING // 2),
                        self.square.width - PADDING, self.square.height - PADDING,
                        self.square.color, corner_radius=self.square.corner_radius, border=self.square.border
                    )

                    sub_square.render(display)

                case CheckboxStyle.CHECKED:
                    start_point = Vector2D(
                        self.square.top_left.x + PADDING,
                        self.square.top_left.y + (self.square.height * 0.75) - PADDING
                    )

                    mid_point = Vector2D(
                        self.square.top_left.x + (self.square.width * 0.25) + PADDING,
                        self.square.top_left.y + self.square.height - PADDING
                    )

                    end_point = Vector2D(
                        self.square.top_left.x + (self.square.width * 0.75) + PADDING,
                        self.square.top_left.y + PADDING
                    )

                    tick_1 = Line(start_point, mid_point, self.square.color, width=3)
                    tick_2 = Line(mid_point, end_point, self.square.color, width=3)

                    tick_1.render(display)
                    tick_2.render(display)

        else:
            self.square.line_width = 3

        self.square.render(display)

        super().render(display)


class CircleCheckbox(Checkbox):
    __slots__ = 'circle'

    def __init__(self, center: Vector2D, radius: int, color: Color, value: bool, children: list[UIElement | Shape],
                 line_width: int = 0, border: Optional[Border] = None, style: CheckboxStyle = CheckboxStyle.SOLID,
                 click_function: Optional[Callable[[], None]] = None, click_event: Optional[Event] = None) -> None:
        super().__init__(value, children, style, click_function, click_event)
        self.circle = Circle(center, radius, color, line_width=line_width, border=border)

    def is_clicked(self) -> bool:
        if mouse.is_clicked(MouseButton.LEFT):
            return bounds.point_within_circle(mouse.position(), self.circle.center, self.circle.radius)

        return False

    def render(self, display: Surface) -> None:
        if self.value:
            match self.style:
                case CheckboxStyle.SOLID:
                    self.circle.line_width = 0

                case CheckboxStyle.BORDERED:
                    sub_circle = Circle(
                        self.circle.center, self.circle.radius - PADDING // 2, self.circle.color,
                        border=self.circle.border
                    )

                    sub_circle.render(display)

                case CheckboxStyle.CHECKED:
                    start_point = Vector2D(
                        self.circle.center.x - self.circle.radius + (PADDING * 2),
                        self.circle.center.y + (self.circle.radius // 2)
                    )

                    mid_point = Vector2D(
                        self.circle.center.x - PADDING,
                        self.circle.center.y + self.circle.radius - PADDING
                    )

                    end_point = Vector2D(
                        self.circle.center.x + self.circle.radius - (PADDING * 2),
                        self.circle.center.y - (self.circle.radius // 2)
                    )

                    tick_1 = Line(start_point, mid_point, self.circle.color, width=3)
                    tick_2 = Line(mid_point, end_point, self.circle.color, width=3)

                    tick_1.add_to_renderer()
                    tick_2.add_to_renderer()

        else:
            self.circle.line_width = 3

        self.circle.render(display)

        super().render(display)


class PolygonCheckbox(Checkbox):
    __slots__ = 'polygon'

    def __init__(self, vertices: list[Vector2D], color: Color, value: bool, children: list[UIElement | Shape],
                 line_width: int = 0, border: Optional[Border] = None, style: CheckboxStyle = CheckboxStyle.SOLID,
                 click_function: Optional[Callable[[], None]] = None, click_event: Optional[Event] = None) -> None:
        super().__init__(value, children, style, click_function, click_event)
        self.polygon = Polygon(vertices, color, line_width=line_width, border=border)

    def is_clicked(self) -> bool:
        if mouse.is_clicked(MouseButton.LEFT):
            return bounds.point_within_polygon(mouse.position(), self.polygon.vertices)

        return False

    def render(self, display: Surface) -> None:
        if self.value:
            match self.style:
                case CheckboxStyle.SOLID:
                    self.polygon.line_width = 0

                case CheckboxStyle.BORDERED:
                    raise NotImplementedError('Bordered style not implemented for polygons.')

                case CheckboxStyle.CHECKED:
                    raise NotImplementedError('Checked style not implemented for polygons.')

        else:
            self.polygon.line_width = 3

        self.polygon.render(display)

        super().render(display)
