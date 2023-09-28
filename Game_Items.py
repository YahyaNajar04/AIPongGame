import pygame
from main import WHITE
pygame.init()



# Paddle Class
class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = self.original_px = x
        self.y = self.original_py = y
        self.width = width
        self.height = height

    def draw(self, win):
        super().__init__()
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        super().__init__()
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset_paddle(self):
        super().__init__()
        self.x = self.original_px
        self.y = self.original_py


# Ball Class
class Ball:
    MAX_VEL = 7
    COLOR = WHITE

    def __init__(self, x, y, radius):
        super().__init__()
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        super().__init__()
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        super().__init__()
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        super().__init__()
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
