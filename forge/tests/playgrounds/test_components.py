from forge.core.engine import color, display, game
from forge.core.managers import event
from forge.core.physics import vector
from forge.hearth.components import checkbox, slider
from forge.hearth.elements import text


class CustomCheckBox:
    __slots__ = 'check_box', 'text_box'

    def __init__(self, check_box: checkbox.Checkbox, text_box: text.Text) -> None:
        self.check_box = check_box
        self.text_box = text_box

    def add_to_default_renderer(self) -> None:
        self.check_box.add_to_renderer()
        self.text_box.add_to_renderer()


class CustomSlider:
    __slots__ = 'slider_comp', 'text_box'

    def __init__(self, slider_comp: slider.Slider, text_box: text.Text) -> None:
        self.slider_comp = slider_comp
        self.text_box = text_box

    def add_to_default_renderer(self) -> None:
        self.slider_comp.add_to_renderer()
        self.text_box.add_to_renderer()


class ComponentTest(game.Game):
    def __init__(self) -> None:
        super().__init__(display.Display(title='Component Tests'))

        self.base_event = event.Event('<BASE-EVENT>')

        self.custom_slider = CustomSlider(
            slider.Slider(0, 100, None, self.base_event, vector.Vector2D(100, 100), 350, color.random(),
                          color.random()),
            text.Text('0', 32, vector.Vector2D(500, 100))
        )

        self.custom_checkbox = CustomCheckBox(
            checkbox.CircularCheckbox(vector.Vector2D(150, 500), 50, color.random(), None, self.base_event),
            text.Text('False', 32, vector.Vector2D(500, 500))
        )

        self.base_event += lambda: self.update_slider(self.custom_slider.slider_comp.value())
        self.base_event += lambda: self.update_checkbox(self.custom_checkbox.check_box.value)

        self.custom_slider.add_to_default_renderer()
        self.custom_checkbox.add_to_default_renderer()

    def update_slider(self, value: float) -> None:
        self.custom_slider.text_box.text = str(round(value, 2))

    def update_checkbox(self, value: bool) -> None:
        self.custom_checkbox.text_box.text = str(value).lower()


def main() -> None:
    component_tests = ComponentTest()
    component_tests.mainloop()


if __name__ == '__main__':
    main()
