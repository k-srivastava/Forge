from forge.core.engine import display, game, game_object, sprite
from forge.core.managers import keyboard
from forge.core.physics import vector
from forge.hearth.elements import text


class Flower(game_object.GameObject):
    def __init__(self, position: vector.Vector2D, asset: str) -> None:
        super().__init__('Flower', position, sprite=sprite.Sprite(asset))

        self.speed = 300
        self.direction = vector.zero()

        self.add_to_renderer()

    def input_manager(self) -> None:
        if keyboard.is_none_pressed():
            self.direction = vector.zero()

        keys = keyboard.get_all_pressed()

        if keys[keyboard.Key.D]:
            self.direction.x = 1

        if keys[keyboard.Key.A]:
            self.direction.x = -1

        if keys[keyboard.Key.W]:
            self.direction.y = -1

        if keys[keyboard.Key.S]:
            self.direction.y = 1

    def wrap_over_display(self) -> None:
        display_width = display.get_display().width()
        display_height = display.get_display().height()

        sprite_width = self.sprite.width()
        sprite_height = self.sprite.height()

        if self.position.x > display_width:
            self.position.x = -sprite_width

        elif self.position.x + sprite_width < 0:
            self.position.x = display_width

        if self.position.y > display_height:
            self.position.y = -sprite_height

        elif self.position.y + sprite_height < 0:
            self.position.y = display_height

    def update(self, delta_time: float) -> None:
        self.direction = vector.Vector2D(1, -1)

        if self.direction.length_squared() != 0:
            self.direction.normalize()

        self.position += self.speed * self.direction * delta_time

        self.wrap_over_display()


class GameObjectTest(game.Game):
    def __init__(self) -> None:
        super().__init__(display.Display(title='Game Object Test'))

        self.flowers = []

        for i in range(6):
            self.flowers.append(Flower(vector.Vector2D(i * 100, i * 100), 'assets/flower.png'))

        title = text.Text('Game Object Test', 64, vector.zero())
        title.center = vector.Vector2D(display.get_display().width() // 2, 120)

        for flower in self.flowers:
            flower.add_to_renderer()
        title.add_to_renderer()

    def update(self) -> None:
        if keyboard.is_clicked(keyboard.Key.SPACE):
            for flower in self.flowers:
                if flower.speed:
                    flower.speed = 0

                else:
                    flower.speed = 300

        if keyboard.is_clicked(keyboard.Key.R):
            for flower in self.flowers:
                flower.speed *= -1

        super().update()


def main():
    game_object_test = GameObjectTest()
    game_object_test.mainloop()


if __name__ == '__main__':
    main()
