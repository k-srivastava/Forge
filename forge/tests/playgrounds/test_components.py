from forge.core.engine import color
from forge.core.engine.display import Display
from forge.core.engine.game import Game
from forge.core.physics.vector import Vector2D
from forge.hearth.components.button import RectangleButton
from forge.hearth.components.checkbox import CheckboxStyle, SquareCheckbox
from forge.hearth.components.slider import Slider


class SliderTest(Game):
    def __init__(self) -> None:
        super().__init__(Display(title='New Slider Tests'))

        self.slider = Slider(0, 100, Vector2D(100, 100), 350, color.random(), color.random(), [],
                             move_function=self.calc)

        self.square_box = SquareCheckbox(
            Vector2D(100, 500), 100, color.random(), False, [],
            style=CheckboxStyle.BORDERED, corner_radius=10
        )

        self.slider.add_to_renderer()
        self.square_box.add_to_renderer()

    def calc(self) -> None:
        print(self.slider.value_clamped)


class ButtonTest(Game):
    def __init__(self) -> None:
        super().__init__(Display(title='New Button Tests'))

        self.button = RectangleButton(
            Vector2D(100, 100), 300, 200, color.random(), 'Click me!', [], click_function=lambda: print('Hello, world!')
        )

        self.button.add_to_renderer()


def main() -> None:
    # component_tests = SliderTest()
    # component_tests.mainloop()

    button_tests = ButtonTest()
    button_tests.mainloop()


if __name__ == '__main__':
    main()
