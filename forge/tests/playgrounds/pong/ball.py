import random

import settings
from forge.core.engine import color, display
from forge.core.managers import event
from forge.core.physics import vector
from forge.hearth.elements import base, shapes


class Ball:
    def __init__(self) -> None:
        self.direction = vector.Vector2D(random.choice((-1, 1)), random.choice((-1, 1)))
        self.direction.normalize()

        self.shape = shapes.Circle(
            vector.Vector2D(settings.DISPLAY_WIDTH // 2, settings.DISPLAY_HEIGHT // 2),
            settings.BALL_RADIUS,
            color.Color(0, 0, 0),
            border=base.Border(5, color.Color(255, 255, 255), settings.BALL_RADIUS)
        )

        self.out_left = event.Event('<BALL-OUT-LEFT>', [self.reset])
        self.out_right = event.Event('<BALL-OUT-RIGHT>', [self.reset])

    def add_to_renderer(self) -> None:
        display.get_display().master_renderer._core_renderer.shapes.append(self.shape)

    def resolve_wall_collisions(self) -> None:
        if self.shape.center.x - self.shape.radius <= 0:
            self.out_left.post()

        elif self.shape.center.x + self.shape.radius >= settings.DISPLAY_WIDTH:
            self.out_right.post()

        if self.shape.center.y - self.shape.radius <= 0:
            self.direction.reflect(vector.down())

        elif self.shape.center.y + self.shape.radius >= settings.DISPLAY_HEIGHT:
            self.direction.reflect(vector.up())

    def resolve_paddle_collisions(
            self,
            player_paddle_shape: shapes.Rectangle, enemy_paddle_shape: shapes.Rectangle
    ) -> None:
        if self.shape.center.x - self.shape.radius <= player_paddle_shape.top_left.x + player_paddle_shape.width:
            if player_paddle_shape.top_left.y <= self.shape.center.y - self.shape.radius <= player_paddle_shape.top_left.y + player_paddle_shape.height:
                self.direction.reflect(vector.right())
                return

        if self.shape.center.x + self.shape.radius >= enemy_paddle_shape.top_left.x:
            if enemy_paddle_shape.top_left.y <= self.shape.center.y - self.shape.radius <= enemy_paddle_shape.top_left.y + enemy_paddle_shape.height:
                self.direction.reflect(vector.left())
                return

    def move(self, velocity: float = 0.5) -> None:
        self.shape.center += self.direction * velocity

    def reset(self) -> None:
        self.direction = vector.Vector2D(random.choice((-1, 1)), random.choice((-1, 1)))
        self.direction.normalize()

        self.shape.center = vector.Vector2D(settings.DISPLAY_WIDTH // 2, settings.DISPLAY_HEIGHT // 2)
