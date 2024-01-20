from abc import ABC, abstractmethod
from math import sqrt
from typing import Type

from forge.hearth.elements.base import Shape
from forge.hearth.elements.shapes import Circle, Polygon, Rectangle


class DimensionalConstraint(ABC):
    def __init__(self, child: Shape, parent: Shape, ratio: float) -> None:
        self.child = child
        self.parent = parent
        self.ratio = ratio

        self._child_type: Type[Shape] = type(child)

    @abstractmethod
    def calculate(self) -> float:
        ...

    @abstractmethod
    def apply(self) -> None:
        ...


class WidthConstraint(DimensionalConstraint):
    def __init__(self, child: Shape, parent: Shape, ratio: float) -> None:
        super().__init__(child, parent, ratio)

    def calculate(self) -> float:
        return self.parent.computed_width() * self.ratio

    def apply(self) -> None:
        if self._child_type is Rectangle:
            self.child.width = self.calculate()

        elif self._child_type is Circle:
            self.child.radius = self.calculate() / 2

        elif self._child_type is Polygon:
            raise NotImplementedError('Not implemented width constraint for child polygon.')

        else:
            raise TypeError('Invalid shape entered.')


class HeightConstraint(DimensionalConstraint):
    def __init__(self, child: Shape, parent: Shape, ratio: float) -> None:
        super().__init__(child, parent, ratio)

    def calculate(self) -> float:
        return self.parent.computed_height() * self.ratio

    def apply(self) -> None:
        if self._child_type is Rectangle:
            self.child.height = self.calculate()

        elif self._child_type is Circle:
            self.child.radius = self.calculate() / 2

        elif self._child_type is Polygon:
            raise NotImplementedError('Not implemented width constraint for child polygon.')

        else:
            raise TypeError('Invalid shape entered.')


class AreaConstraint(DimensionalConstraint):
    def __init__(self, child: Shape, parent: Shape, ratio: float) -> None:
        super().__init__(child, parent, ratio)

    def calculate(self) -> float:
        return self.parent.area * self.ratio

    def apply(self) -> None:
        if self._child_type is Rectangle:
            length_delta: float = sqrt(self.calculate())

            self.child.height = length_delta
            self.child.width = length_delta

        elif self._child_type is Circle:
            pass

        elif self._child_type is Polygon:
            raise NotImplementedError('Not implemented width constraint for child polygon.')

        else:
            raise TypeError('Invalid shape entered.')
