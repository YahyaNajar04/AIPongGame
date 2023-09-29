import pygame
import movements
import DrawItems
from Game_Items import Paddle, Ball
from movements import movement

pygame.init()

# Defining the Screen
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
WINNING_SCORE = 5

# Defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setting FPS
FPS = 60

# Defining height and width of paddles
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

ai_paddle = movements.AIPaddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)


# Main game loop
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        DrawItems.draw(WIN, [left_paddle, ai_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        movement.handle_paddle_movement(keys, left_paddle, right_paddle)
        movement.handle_collision(ball, left_paddle, ai_paddle)
        ball.move()
        ai_paddle.move_ai(ball)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset_paddle()
            right_paddle.reset_paddle()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset_paddle()
            right_paddle.reset_paddle()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "You Won!"
            movements.Winning_Sound.play()
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "AI Wins!"
            movements.Winning_Sound.play()

        if won:
            text = DrawItems.SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            right_paddle.reset_paddle()
            left_paddle.reset_paddle()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == "__main__":
    main()
