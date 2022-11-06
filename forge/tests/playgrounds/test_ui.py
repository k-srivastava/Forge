from forge.core.engine import color, display, game
from forge.core.managers import keyboard
from forge.core.physics import vector
from forge.hearth.elements import shapes, text


class UITest(game.Game):
    def __init__(self) -> None:
        super().__init__(display.Display(title='UI Tests'))

        self.hello_world = text.Text('Hello, world!', 32)
        self.circle = shapes.Circle(vector.Vector2D(300, 300), 100, color.random(),
                                    border=shapes.Border(10, color.random()))

        self.circle.add_to_renderer()
        self.hello_world.add_to_renderer()

    def update(self) -> None:
        displacement = 1
        direction = vector.zero()

        if keyboard.is_any_pressed():
            if keyboard.is_pressed(keyboard.Key.W):
                direction.y = -1

            elif keyboard.is_pressed(keyboard.Key.S):
                direction.y = 1

            if keyboard.is_pressed(keyboard.Key.A):
                direction.x = -1

            elif keyboard.is_pressed(keyboard.Key.D):
                direction.x = 1

            direction.normalize()

        else:
            direction = vector.zero()

        self.circle.center += direction * displacement

        super().update()


def main() -> None:
    ui_tests = UITest()
    ui_tests.mainloop()


if __name__ == '__main__':
    main()
