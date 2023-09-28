import pygame

pygame.init()

# Defining the Screen
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

# Defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setting FPS
FPS = 60

# Defining height and width of paddles
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# Playing Sounds
Ball_Bounce_Sound = pygame.mixer.Sound('4391__noisecollector__pongblipf5.wav')
Winning_Sound = pygame.mixer.Sound('582988__oysterqueen__success.mp3')


class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_px = x
        self.y = self.original_py = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset_paddle(self):
        self.x = self.original_px
        self.y = self.original_py


# Ball class
class Ball:
    MAX_VEL = 7
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


class AIPaddle(Paddle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def move_ai(self, ball):
        if ball.y < self.y + self.height // 2 and ball.y >= 0:
            self.move(up=True)
        elif ball.y > self.y + self.height // 2:
            self.move(up=False)


ai_paddle = AIPaddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)


# Drawing items
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)

    pygame.display.update()


# Function to handle collision
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
        draw(WIN, [left_paddle, ai_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_collision(ball, left_paddle, ai_paddle)
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
            Winning_Sound.play()
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "AI Wins!"
            Winning_Sound.play()

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
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
