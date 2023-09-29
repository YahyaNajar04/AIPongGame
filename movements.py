import pygame
from Game_Items import Paddle, Ball

WIDTH, HEIGHT = 700, 500
BALL_RADIUS = 7

# Playing Sounds
Ball_Bounce_Sound = pygame.mixer.Sound('4391__noisecollector__pongblipf5.wav')
Winning_Sound = pygame.mixer.Sound('582988__oysterqueen__success.mp3')


class movement():
    def handle_collision(ball, left_paddle, ai_paddle):
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
            Ball_Bounce_Sound.play()
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1
            Ball_Bounce_Sound.play()

        if ball.x_vel < 0:
            if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + left_paddle.height // 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height // 2) / Ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    Ball_Bounce_Sound.play()

        else:
            if ai_paddle.y <= ball.y <= ai_paddle.y + ai_paddle.height:
                if ball.x + ball.radius >= ai_paddle.x:
                    ball.x_vel *= -1
                    middle_y = ai_paddle.y + ai_paddle.height // 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (ai_paddle.height // 2) / Ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    Ball_Bounce_Sound.play()

    # Function to move paddles
    def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL < HEIGHT - left_paddle.height:
            left_paddle.move(up=False)
        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL < HEIGHT - right_paddle.height:
            right_paddle.move(up=False)


class AIPaddle(Paddle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def move_ai(self, ball):
        if self.y + self.height // 2 > ball.y >= 0:
            self.move(up=True)
        elif ball.y > self.y + self.height // 2:
            self.move(up=False)
