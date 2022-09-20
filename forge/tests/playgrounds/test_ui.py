from forge.core.engine import color, display, game
from forge.core.physics import vector
from forge.hearth.elements import shapes, text


def main() -> None:
    test_ui = game.Game(display.Display(800, 800, 'UI Tests', 120))

    circle = shapes.Circle(vector.Vector2D(300, 300), 100, color.random())
    circle.add_to_renderer()

    box = text.Text('Hello, world!', 32)
    box.add_to_renderer()

    test_ui.mainloop()


if __name__ == '__main__':
    main()
