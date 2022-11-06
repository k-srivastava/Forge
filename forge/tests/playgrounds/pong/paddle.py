import settings
from forge.core.engine import color, constants
from forge.core.managers import keyboard
from forge.core.physics import vector
from forge.core.utils import math
from forge.hearth.elements import shapes


class Paddle:
    def __init__(self, is_player: bool) -> None:
        self.is_player = is_player

        self.direction = vector.zero()
        self.shape = shapes.Rectangle(
            vector.Vector2D(100, (settings.DISPLAY_HEIGHT - settings.PADDLE_HEIGHT) // 2),
            settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT,
            color.Color(255, 255, 255)
        )

        if not is_player:
            self.shape.top_left.x = settings.DISPLAY_WIDTH - (100 + settings.PADDLE_WIDTH)

    def add_to_renderer(self, renderer_name: str = constants.DISPLAY_UI_RENDERER) -> None:
        self.shape.add_to_renderer(renderer_name)

    def poll_inputs(self) -> None:
        if not self.is_player:
            return

        if keyboard.is_any_pressed():
            if keyboard.is_pressed(keyboard.Key.W) or keyboard.is_pressed(keyboard.Key.UP):
                self.direction.y = -1

            if keyboard.is_pressed(keyboard.Key.S) or keyboard.is_pressed(keyboard.Key.DOWN):
                self.direction.y = 1

        else:
            self.direction.y = 0

    def move(self, velocity: int = 1, y_position: int | None = None) -> None:
        if not self.is_player:
            if y_position < self.shape.center.y:
                self.direction.y = -1

            elif y_position > self.shape.center.y:
                self.direction.y = 1

            else:
                self.direction.y = 0

        self.shape.center += self.direction * velocity
        self.shape.top_left.y = math.clamp(self.shape.top_left.y, 0, settings.DISPLAY_HEIGHT - self.shape.height)
