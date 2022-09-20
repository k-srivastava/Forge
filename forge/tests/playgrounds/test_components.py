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


def main() -> None:
    def update_checkbox_text(text_box: text.Text, value: bool) -> None:
        text_box.text = str(value)

    def update_slider_text(text_box: text.Text, value: float) -> None:
        text_box.text = str(round(value, 2))

    test_components = game.Game(display.Display(800, 800, 'Component Tests', 120))

    base_event = event.Event('<BASE-EVENT>')

    custom_checkbox = CustomCheckBox(
        checkbox.CircleCheckbox(
            vector.Vector2D(100, 500), 50, color.random(), base_event, style=checkbox.CheckboxStyle.CHECKED
        ),
        text.Text('False', 32, vector.Vector2D(500, 500))
    )

    custom_slider = CustomSlider(
        slider.Slider(0, 100, base_event, vector.Vector2D(100, 100), 350, color.random(), color.random()),
        text.Text('0', 32, vector.Vector2D(500, 100))
    )

    base_event += lambda: update_checkbox_text(custom_checkbox.text_box, custom_checkbox.check_box.value)
    base_event += lambda: update_slider_text(custom_slider.text_box, custom_slider.slider_comp.value())

    custom_checkbox.add_to_default_renderer()
    custom_slider.add_to_default_renderer()

    test_components.mainloop()


if __name__ == '__main__':
    main()
