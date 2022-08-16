"""
RGBA colors in Forge.
"""
from __future__ import annotations

import dataclasses
import random as rand

import pygame


@dataclasses.dataclass(slots=True)
class Color:
    """
    Forge's representation of an 8-bit RGBA color.
    """
    red: int
    green: int
    blue: int
    alpha: int = 255

    def __post_init__(self) -> None:
        """
        Confirm whether the values supplied to the color lie in the 8-bit RGBA spectrum.
        """
        _confirm_color_bounds(self)

    def __add__(self, other: Color) -> Color:
        """
        Add two colors together using the '+' operator.

        :param other: Other color to be added.
        :type other: Color

        :return: Color with each component as the sum of the individual components of the colors.
        :rtype: Color

        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        try:
            return Color(
                self.red + other.red, self.green + other.green, self.blue + other.blue,
                self.alpha + other.alpha
            )

        # Except and re-raise the error.
        except ValueError as e:
            raise e

    def __iadd__(self, other: Color) -> Color:
        """
        Add one color to another color in-place using the '+=' operator.

        :param other: Other color to be added.
        :type other: Color

        :return: Color with each component as the sum of the individual components of the colors.
        :rtype: Color

        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        self.red += other.red
        self.green += other.green
        self.blue += other.blue
        self.alpha += other.alpha

        _confirm_color_bounds(self)
        return self

    def __sub__(self, other: Color) -> Color:
        """
        Subtract two colors from each other using the '-' operator.

        :param other: Other color to be subtracted.
        :type other: Color

        :return: Color with each component as the difference of the individual components of the colors.
        :rtype: Color

        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        try:
            return Color(
                self.red - other.red, self.green - other.green, self.blue - other.blue,
                self.alpha - other.alpha
            )

        # Except and re-raise the error.
        except ValueError as e:
            raise e

    def __isub__(self, other: Color) -> Color:
        """
        Subtract one color from another color in-place using the '-=' operator.

        :param other: Other color to be subtracted.
        :type other: Color

        :return: Color with each component as the difference of the individual components of the colors.
        :rtype: Color

        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        self.red -= other.red
        self.green -= other.green
        self.blue -= other.blue
        self.alpha -= other.alpha

        _confirm_color_bounds(self)
        return self

    def __mul__(self, factor: int) -> Color:
        """
        Multiply a color by a given value on all components using the '*' operator.

        :param factor: Factor by which the components of the color are to be multiplied.
        :type factor: int

        :return: Color with each component multiplied by the factor.
        :rtype: Color

        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        try:
            return Color(self.red * factor, self.green * factor, self.blue * factor, self.alpha * factor)

        # Except and re-raise the error.
        except ValueError as e:
            raise e

    def __imul__(self, factor: int) -> Color:
        """
        Multiply a color in-place by a given value on all components using the '*=' operator.

        :param factor: Factor by which the components of the color are to be multiplied.
        :type factor: int

        :return: Color with each component multiplied by the factor.
        :rtype: Color

        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        self.red *= factor
        self.green *= factor
        self.blue *= factor
        self.alpha *= factor

        _confirm_color_bounds(self)
        return self

    def __floordiv__(self, factor: int) -> Color:
        """
        Floor divide a color by a given value on all components using the '//' operator.

        :param factor: Factor by which the components of the color are to be floor divided.
        :type factor: int

        :return: Color with each component floor divided by the factor.
        :rtype: Color

        :raises ZeroDivisionError: Components of the color cannot be divided by zero.
        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        if factor == 0:
            raise ZeroDivisionError('Cannot divide a color by zero.')

        try:
            return Color(self.red // factor, self.green // factor, self.blue // factor, self.alpha // factor)

        # Except and re-raise the error.
        except ValueError as e:
            raise e

    def __ifloordiv__(self, factor: int) -> Color:
        """
        Floor divide a color in-place by a given value on all components using the '//=' operator.

        :param factor: Factor by which the components of the color are to be floor divided.
        :type factor: int

        :return: Color with each component floor divided by the factor.
        :rtype: Color

        :raises ZeroDivisionError: Components of the color cannot be divided by zero.
        :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
        """
        if factor == 0:
            raise ZeroDivisionError('Cannot divide a vector by zero.')

        self.red //= factor
        self.green //= factor
        self.blue //= factor
        self.alpha //= factor

        _confirm_color_bounds(self)
        return self

    def __bool__(self) -> bool:
        """
        Convert the color into a boolean.

        :return: False if all the components are equal to zero; else True.
        :rtype: bool
        """
        return not (self.red == self.green == self.blue == 0)

    def __copy__(self) -> Color:
        """
        Create a shallow copy of the color by copying all the components into a new color.

        :return: Shallow copy of the color.
        :rtype: Color
        """
        return Color(self.red, self.green, self.blue, self.alpha)

    def __repr__(self) -> str:
        """
        Internal representation of the color.

        :return: Simple string with values of all components of the color.
        :rtype: str
        """
        return f'Color -> R: {self.red}, G: {self.green}, B: {self.blue}, A: {self.alpha}'

    def __str__(self) -> str:
        """
        String representation of the color.

        :return: Detailed string with values of all components of the color.
        :rtype: str
        """
        return f'Forge ColorRGBA -> red: {self.red}, green: {self.green}, blue: {self.blue}, alpha: {self.alpha}'

    def as_tuple(self, with_alpha: bool = False) -> tuple[int, int, int] | tuple[int, int, int, int]:
        """
        Return the R, G, B and (optionally) A components of the Color in a tuple. Beneficial for internal
        interoperability with Pygame.

        :param with_alpha: Whether to include the alpha values in the tuple.
        :type with_alpha: bool

        :return: Tuple of the color's R, G, B and (optionally) A components respectively.
        :rtype: tuple[int, int, int] | tuple[int, int, int, int]
        """
        if with_alpha:
            return self.red, self.green, self.blue, self.alpha

        return self.red, self.green, self.blue

    def as_pygame_color(self) -> pygame.color.Color:
        """
        Return the color as a Pygame color. Beneficial for internal interoperability with Pygame.

        :return: Pygame color from the color's R, G, B and A components respectively.
        :rtype: pygame.color.Color
        """
        return pygame.color.Color(self.red, self.green, self.blue, self.alpha)


def random(with_alpha: bool = False) -> Color:
    """
    Create a new random color.

    :param with_alpha: Whether to include the alpha value during the random number generation.
    :type with_alpha: bool

    :return: New random color.
    :rtype: Color
    """
    red: int = rand.randint(0, 255)
    green: int = rand.randint(0, 255)
    blue: int = rand.randint(0, 255)
    alpha = 255

    if with_alpha:
        alpha = rand.randint(0, 255)

    return Color(red, green, blue, alpha)


def _confirm_color_bounds(color: Color) -> None:
    """
    Confirm whether a Forge color's R, G, B and A components lie within the 8-bit color range (0-255).

    :param color: Color whose bounds are to be checked.
    :type color: Color

    :raises ValueError: Forge colors can only have 8-bit values for the R, G, B and A components.
    """

    if color.red in range(256) and color.green in range(256) and color.blue in range(256) and color.alpha in range(256):
        return

    raise ValueError(
        'RGBA colors can only have values between 0 and 255 (inclusive), '
        f'not: {color.red, color.green, color.blue, color.alpha}.'
    )
