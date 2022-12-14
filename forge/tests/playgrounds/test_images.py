from forge.core.engine import display, game, image, sprite
from forge.core.managers import keyboard, mouse
from forge.core.physics import vector


class ImageTest(game.Game):
    def __init__(self, display_: display.Display) -> None:
        super().__init__(display_)
        self.flower_pool = image.ImagePool('<FLOWER-IMAGE-POOL>')
        self.flower_index = 0

        self.flower_pool.add_to_renderer()

    def update(self) -> None:
        if mouse.is_pressed(mouse.MouseButton.LEFT):
            self.spawn_image(mouse.position())

        if mouse.is_pressed(mouse.MouseButton.RIGHT):
            self.delete_image()

        if keyboard.is_any_clicked():
            self.spawn_image(mouse.position())

        super().update()

    def spawn_image(self, position: vector.Vector2D) -> None:
        self.flower_pool += image.Image('assets/flower.png', position, f'Flower-{self.flower_index}')
        self.flower_index += 1

    def delete_image(self) -> None:
        image_name = f'Flower-{self.flower_index - 1}'

        try:
            self.flower_pool -= image.get_image_from_name(image_name)
            image.delete_image_from_name(image_name)
            self.flower_index -= 1

        except ValueError:
            pass

        except KeyError:
            pass


def main() -> None:
    icon_sprite = sprite.Sprite('assets/flower.png')
    image_tests = ImageTest(display.Display(title='Image Tests', icon=icon_sprite))
    image_tests.mainloop()


if __name__ == '__main__':
    main()
