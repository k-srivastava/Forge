from forge.core.engine.color import Color
from forge.core.engine.display import Display
from forge.core.engine.game import Game
from forge.core.managers import keyboard
from forge.core.managers.keyboard import Key
from forge.core.physics.vector import Vector2D
from forge.hearth.constraints.dimensional import AreaConstraint, HeightConstraint, WidthConstraint
from forge.hearth.elements.shapes import Rectangle
from forge.core.utils import math as forge_math


class DimensionalConstraintsTest(Game):
    def __init__(self) -> None:
        super().__init__(Display(title='Dimensional Constraints Tests'))

        self.parent_rect = Rectangle(
            Vector2D(100, 100), 500, 500, Color(255, 10, 10)
        )

        self.child_rect = Rectangle(
            Vector2D(0, 0), 450, 450, Color(10, 255, 10), self.parent_rect
        )

        # self.area_constraint = AreaConstraint(self.child_rect, self.parent_rect, 0.9)

        self.width_constraint = WidthConstraint(self.child_rect, self.parent_rect, 0.9)
        self.height_constraint = HeightConstraint(self.child_rect, self.parent_rect, 0.9)

        self.parent_rect.add_to_renderer()
        self.child_rect.add_to_renderer()

    def update(self) -> None:
        speed = 0.5
        if keyboard.is_pressed(Key.W):
            self.parent_rect.top_left.y -= speed

        if keyboard.is_pressed(Key.A):
            self.parent_rect.top_left.x -= speed

        if keyboard.is_pressed(Key.S):
            self.parent_rect.top_left.y += speed

        if keyboard.is_pressed(Key.D):
            self.parent_rect.top_left.x += speed

        if keyboard.is_pressed(Key.UP):
            self.parent_rect.height -= speed
            # self.height_constraint.apply()

        if keyboard.is_pressed(Key.DOWN):
            self.parent_rect.height += speed
            # self.height_constraint.apply()

        if keyboard.is_pressed(Key.LEFT):
            self.parent_rect.width -= speed
            # self.width_constraint.apply()

        if keyboard.is_pressed(Key.RIGHT):
            self.parent_rect.width += speed
            # self.width_constraint.apply()

        self.width_constraint.apply()
        self.height_constraint.apply()
        # self.area_constraint.apply()

        if self.parent_rect.width <= 20:
            self.parent_rect.width = 20

        if self.parent_rect.height <= 20:
            self.parent_rect.height = 20

        self.child_rect.width = forge_math.clamp(self.child_rect.width, 0, self.parent_rect.width - 20)
        self.child_rect.height = forge_math.clamp(self.child_rect.height, 0, self.parent_rect.height - 20)

        self.child_rect.center = self.parent_rect.center

        super().update()


def main() -> None:
    dimensional_constraints_test = DimensionalConstraintsTest()
    dimensional_constraints_test.mainloop()


if __name__ == '__main__':
    main()
