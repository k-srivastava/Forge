"""Buttons in Hearth."""
from abc import abstractmethod
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
from forge.hearth.elements.shapes import Circle, Polygon, Rectangle
from forge.hearth.elements.text import Text
from forge.hearth.settings import DEFAULT_FONT_FACE, DEFAULT_FONT_SIZE
from forge.hearth.utils import bounds


class Button(UIComponent):
    __slots__ = 'text', 'click_function', 'click_event', '_text_centered'

    def __init__(self, text: str, children: list[UIElement | Shape], font_size: int = DEFAULT_FONT_SIZE,
                 font_face: str = DEFAULT_FONT_FACE, text_color: Color = Color(255, 255, 255),
                 text_background_color: Optional[Color] = None, anti_aliasing: bool = True, text_centered: bool = True,
                 click_function: Optional[Callable[[], None]] = None, click_event: Optional[Event] = None) -> None:
        super().__init__(children)

        self.text = Text(
            text, Vector2D.zero(), font_size, font_face, text_color, text_background_color,
            anti_aliasing=anti_aliasing
        )

        self.click_function = click_function
        self.click_event = click_event

        self._text_centered = text_centered

    def __repr__(self) -> str:
        return f'Button(text={self.text}, click_function={self.click_function}, click_event={self.click_event}, ' \
               f'text_centered={self._text_centered})'

    @property
    def text_centered(self) -> bool:
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        self._text_centered = value

    @abstractmethod
    def is_clicked(self) -> bool:
        """"""

    def render(self, display: Surface) -> None:
        self.text.render(display)
        super().render(display)

    def update(self) -> None:
        if self.is_clicked():
            if self.click_function is not None:
                self.click_function()

            if self.click_event is not None:
                self.click_event.post()

        self.text.update()
        super().update()


class RectangleButton(Button):
    __slots__ = 'rectangle'

    def __init__(self, top_left: Vector2D, width: int, height: int, color: Color, text: str,
                 children: list[UIElement | Shape], line_width: int = 0, corner_radius: Optional[int] = None,
                 border: Optional[Border] = None, font_size: int = DEFAULT_FONT_SIZE,
                 font_face: str = DEFAULT_FONT_FACE, text_color: Color = Color(255, 255, 255),
                 text_background_color: Optional[Color] = None, anti_aliasing: bool = True, text_centered: bool = True,
                 click_function: Optional[Callable[[], None]] = None, click_event: Optional[Event] = None) -> None:
        super().__init__(
            text, children, font_size, font_face, text_color, text_background_color, anti_aliasing, text_centered,
            click_function, click_event
        )

        self.rectangle = Rectangle(
            top_left, width, height, color, line_width=line_width, corner_radius=corner_radius,
            border=border
        )

        if self._text_centered:
            self.text.center = self.rectangle.center
        else:
            self.text.top_left = self.rectangle.top_left

    @property
    def text_centered(self) -> bool:
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        if value:
            self.text.center = self.rectangle.center
        else:
            self.text.top_left = self.rectangle.top_left

        self._text_centered = value

    def is_clicked(self) -> bool:
        if mouse.is_clicked(MouseButton.LEFT):
            return bounds.point_within_rectangle(
                mouse.position(), self.rectangle.top_left, self.rectangle.width, self.rectangle.height
            )

        return False

    def render(self, display: Surface) -> None:
        self.rectangle.render(display)
        super().render(display)


class CircleButton(Button):
    __slots__ = 'circle'

    def __init__(self, center: Vector2D, radius: int, color: Color, text: str, children: list[UIElement | Shape],
                 line_width: int = 0, border: Optional[Border] = None, font_size: int = DEFAULT_FONT_SIZE,
                 font_face: str = DEFAULT_FONT_FACE, text_color: Color = Color(255, 255, 255),
                 text_background_color: Optional[Color] = None, anti_aliasing: bool = True,
                 text_centered: bool = True, click_function: Optional[Callable[[], None]] = None,
                 click_event: Optional[Event] = None) -> None:
        super().__init__(
            text, children, font_size, font_face, text_color, text_background_color, anti_aliasing, text_centered,
            click_function, click_event
        )

        self.circle = Circle(center, radius, color, line_width=line_width, border=border)

        if self._text_centered:
            self.text.center = self.circle.center
        else:
            self.text.top_left = self.circle.top_left

    @property
    def text_centered(self) -> bool:
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        if value:
            self.text.center = self.circle.center
        else:
            self.text.top_left = self.circle.top_left

        self._text_centered = value

    def is_clicked(self) -> bool:
        if mouse.is_clicked(MouseButton.LEFT):
            return bounds.point_within_circle(mouse.position(), self.circle.center, self.circle.radius)

        return False

    def render(self, display: Surface) -> None:
        self.circle.render(display)
        super().render(display)


class PolygonButton(Button):
    __slots__ = 'polygon'

    def __init__(self, vertices: list[Vector2D], color: Color, text: str, children: list[UIElement | Shape],
                 line_width: int = 0, border: Optional[Border] = None, font_size: int = DEFAULT_FONT_SIZE,
                 font_face: str = DEFAULT_FONT_FACE, text_color: Color = Color(255, 255, 255),
                 text_background_color: Optional[Color] = None, anti_aliasing: bool = True, text_centered: bool = True,
                 click_function: Optional[Callable[[], None]] = None, click_event: Optional[Event] = None) -> None:
        super().__init__(
            text, children, font_size, font_face, text_color, text_background_color, anti_aliasing, text_centered,
            click_function, click_event
        )

        self.polygon = Polygon(vertices, color, line_width=line_width, border=border)

        if self.text_centered:
            self.text.center = self.polygon.center
        else:
            self.text.top_left = self.polygon.top_left

    @property
    def text_centered(self) -> bool:
        return self._text_centered

    @text_centered.setter
    def text_centered(self, value: bool) -> None:
        if value:
            self.text.center = self.polygon.center
        else:
            self.text.top_left = self.polygon.top_left

        self._text_centered = value

    def is_clicked(self) -> bool:
        if mouse.is_clicked(MouseButton.LEFT):
            return bounds.point_within_polygon(mouse.position(), self.polygon.vertices)

        return False

    def render(self, display: Surface) -> None:
        self.polygon.render(display)
        super().render(display)
