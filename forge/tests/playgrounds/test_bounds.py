from forge.core.engine import color, display, game
from forge.core.managers import keyboard
from forge.core.physics import vector
from forge.hearth.elements import shapes
from forge.hearth.utils import bounds


class BoundsTest(game.Game):
    def __init__(self) -> None:
        super().__init__(display.Display(title='Bounds Test'))

        self.polygon = shapes.Polygon(
            [vector.Vector2D(300, 300), vector.Vector2D(700, 700), vector.Vector2D(300, 700),
             vector.Vector2D(700, 300)],
            color.random()
        )

        self.circle = shapes.Circle(vector.Vector2D(100, 200), 50, color.Color(255, 255, 255))
        self.rectangle = shapes.Rectangle(vector.Vector2D(300, 300), 600, 400, color.random())

        self.rectangle.add_to_renderer()
        self.circle.add_to_renderer()

    def update(self) -> None:
        if keyboard.is_pressed(keyboard.Key.D):
            self.circle.center.x += 1

        if keyboard.is_pressed(keyboard.Key.A):
            self.circle.center.x -= 1

        if keyboard.is_pressed(keyboard.Key.S):
            self.circle.center.y += 1

        if keyboard.is_pressed(keyboard.Key.W):
            self.circle.center.y -= 1

        if bounds.point_within_rectangle(self.circle.center, self.rectangle.top_left, self.rectangle.width,
                                         self.rectangle.height):
            self.circle.color = color.Color(255, 50, 50)
        else:
            self.circle.color = color.Color(255, 255, 255)

        super().update()


def main() -> None:
    bounds_test = BoundsTest()
    bounds_test.mainloop()


if __name__ == '__main__':
    main()
