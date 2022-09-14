from random import randint

from forge.core.engine import display, game
from forge.core.physics import vector
from forge.hearth.elements import debug


def rand() -> int:
    return randint(0, 800)


class DebugTest(game.Game):
    def __init__(self, display_: display.Display) -> None:
        super().__init__(display_)

    def render(self) -> None:
        super().render()

        debug.draw_line(vector.Vector2D(rand(), rand()), vector.Vector2D(rand(), rand()))
        debug.draw_rectangle(vector.Vector2D(rand(), rand()), randint(0, 200), randint(0, 200))
        debug.draw_circle(vector.Vector2D(rand(), rand()), randint(0, 200))


def main() -> None:
    debug_tests = DebugTest(display.Display(800, 800, 'Debug Tests', 120))
    debug_tests.mainloop()


if __name__ == '__main__':
    main()
