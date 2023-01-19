import ball
import paddle
import settings
from forge.core.engine import color, display, game, timer
from forge.core.physics import vector
from forge.hearth.elements import shapes, text


class Pong(game.Game):
    def __init__(self) -> None:
        super().__init__(
            display.Display(
                width=settings.DISPLAY_WIDTH, height=settings.DISPLAY_HEIGHT,
                title='Pong',
                background_color=color.Color(0, 0, 0)
            )
        )

        self.player_score = 0
        self.enemy_score = 0
        self.ball_velocity = 1

        self.timer = timer.Timer()

        self.player_paddle = paddle.Paddle(is_player=True)
        self.enemy_paddle = paddle.Paddle(is_player=False)
        self.ball = ball.Ball()

        self.ui = [
            shapes.Line(
                vector.Vector2D(settings.DISPLAY_WIDTH // 2, 0),
                vector.Vector2D(settings.DISPLAY_WIDTH // 2, settings.DISPLAY_HEIGHT),
                color.Color(255, 255, 255)
            ),

            text.Text(str(self.player_score), font_size=64, top_left=vector.Vector2D(settings.DISPLAY_WIDTH / 3, 50)),
            text.Text(str(self.enemy_score), font_size=64, top_left=vector.Vector2D(settings.DISPLAY_WIDTH * 2 / 3, 50))
        ]

        self.ui_win_text = text.Text('', font_size=72)

        self.player_paddle.add_to_renderer()
        self.enemy_paddle.add_to_renderer()
        self.ball.add_to_renderer()

        for ui in self.ui:
            self.display.master_renderer._ui_renderer.elements.append(ui)

        self.ball.out_left += self.enemy_scores
        self.ball.out_right += self.player_scores

        self.timer.start()

    def player_scores(self) -> None:
        self.player_score += 1
        self.ui[1].text = str(self.player_score)
        self.ball_velocity = 1

    def enemy_scores(self) -> None:
        self.enemy_score += 1
        self.ui[2].text = str(self.enemy_score)
        self.ball_velocity = 1

    def check_win_condition(self) -> None:
        if self.player_score == settings.WIN_SCORE or self.enemy_score == settings.WIN_SCORE:
            self.ball.reset()
            self.ball.direction = vector.zero()
            self.ball.shape.border.color = color.Color(0, 0, 0)

            if self.player_score == settings.WIN_SCORE:
                self.ui_win_text.text = 'Player wins!'

            elif self.enemy_score == settings.WIN_SCORE:
                self.ui_win_text.text = 'Enemy wins!'

            self.ui_win_text.center = vector.Vector2D(settings.DISPLAY_WIDTH // 2, settings.DISPLAY_HEIGHT // 2)
            self.display.master_renderer._ui_renderer.elements.append(self.ui_win_text)
            self.timer.stop()

    def update(self) -> None:
        try:
            if self.timer.time() > 5:
                self.ball_velocity += 0.05
                self.timer.reset()

        except RuntimeError:
            pass

        self.player_paddle.poll_inputs()

        self.ball.resolve_wall_collisions()
        self.ball.resolve_paddle_collisions(self.player_paddle.shape, self.enemy_paddle.shape)

        self.player_paddle.move()
        self.enemy_paddle.move(y_position=self.ball.shape.center.y)
        self.ball.move(self.ball_velocity)

        self.check_win_condition()

        super().update()


def main() -> None:
    pong = Pong()
    pong.mainloop()


if __name__ == '__main__':
    main()
