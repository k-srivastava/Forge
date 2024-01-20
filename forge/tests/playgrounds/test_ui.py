from forge.core.engine.color import Color
from forge.core.engine.display import Display
from forge.core.engine.game import Game
from forge.core.managers import keyboard
from forge.core.physics.vector import Vector2D
from forge.hearth.elements.shapes import Circle, Polygon, Rectangle
from forge.hearth.elements.text import Text


class UITest(Game):
    def __init__(self) -> None:
        super().__init__(Display(title='UI Tests'))

        self.title = Text('UI Test', Vector2D.zero(), 64)
        self.title.center = Vector2D(self.display.width() // 2, 100)

        self.chassis = Rectangle(Vector2D(100, 100), 350, 150, Color(255, 80, 80))
        self.window = Rectangle(Vector2D(300, 0), 50, 20, Color(80, 255, 255), parent=self.chassis)
        self.wheel_1 = Circle(Vector2D(60, 150), 50, Color(50, 50, 50), parent=self.chassis)
        self.wheel_2 = Circle(Vector2D(290, 150), 50, Color(50, 50, 50), parent=self.chassis)

        self.title.add_to_renderer()
        self.chassis.add_to_renderer()

        self.polygon = Polygon([Vector2D(100, 100), Vector2D(100, 300), Vector2D(300, 300)], Color(0, 100, 255))
        self.polygon.add_to_renderer()

    def update(self) -> None:
        if keyboard.is_pressed(keyboard.Key.D):
            self.chassis.top_left += Vector2D.right()
            self.polygon.center += Vector2D.right()

        super().update()


def main() -> None:
    ui_tests = UITest()
    ui_tests.mainloop()


if __name__ == '__main__':
    main()
