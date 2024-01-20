"""Sliders in Hearth."""
from typing import Callable, Optional

from forge.core.engine.color import Color
from forge.core.managers import mouse
from forge.core.managers.event import Event
from forge.core.managers.mouse import MouseButton
from forge.core.physics.vector import Vector2D
from forge.core.utils import math as forge_math
from forge.core.utils.aliases import Surface
from forge.hearth.components.base import UIComponent
from forge.hearth.elements.base import Shape, UIElement
from forge.hearth.elements.border import Border
from forge.hearth.elements.shapes import Circle, Rectangle
from forge.hearth.settings import PADDING
from forge.hearth.utils import bounds


class Slider(UIComponent):
    __slots__ = 'start_value', 'end_value', 'move_function', 'move_event', 'bar', 'grabber'

    def __init__(self, start_value: float, end_value: float, top_left: Vector2D, bar_width: int, bar_color: Color,
                 grabber_color: Color, children: list[UIElement | Shape],
                 bar_height: int = 10, bar_line_width: int = 0, grabber_radius: int = 15, grabber_line_width: int = 0,
                 bar_corner_radius: Optional[int] = None, bar_border: Optional[Border] = None,
                 grabber_border: Optional[Border] = None, move_function: Optional[Callable[[], None]] = None,
                 move_event: Optional[Event] = None) -> None:
        super().__init__(children)

        if end_value <= start_value:
            raise ValueError(f'The end value {end_value} cannot be greater than the start value {start_value}.')

        self.start_value = start_value
        self.end_value = end_value

        self.move_function = move_function
        self.move_event = move_event

        self.bar = Rectangle(
            top_left, bar_width, bar_height, bar_color, line_width=bar_line_width,
            corner_radius=bar_corner_radius, border=bar_border
        )

        self.grabber = Circle(Vector2D(
            top_left.x, top_left.y + bar_height // 2), grabber_radius, grabber_color,
            line_width=grabber_line_width, border=grabber_border
        )

    @property
    def value(self) -> float:
        return (self.grabber.center.x - self.bar.top_left.x) * (self.end_value - self.start_value) / self.bar.width

    @property
    def value_clamped(self) -> float:
        return (self.grabber.center.x - self.bar.top_left.x) / self.bar.width

    def is_moved(self) -> bool:
        if mouse.is_pressed(MouseButton.LEFT):
            if bounds.point_within_rectangle(
                    mouse.position(),
                    Vector2D(self.bar.top_left.x - PADDING, self.bar.top_left.y - self.grabber.radius),
                    self.bar.width + PADDING, self.grabber.radius * 2
            ):
                return True

        return False

    def render(self, display: Surface) -> None:
        self.bar.render(display)
        self.grabber.render(display)

        super().render(display)

    def update(self) -> None:
        if self.is_moved():
            self.grabber.center.x = forge_math.clamp(
                mouse.position().x, self.bar.top_left.x,
                self.bar.top_left.x + self.bar.width
            )

            if self.move_function is not None:
                self.move_function()

            if self.move_event is not None:
                self.move_event.post()

        self.bar.update()
        self.grabber.update()

        super().update()
