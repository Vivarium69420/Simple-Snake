import random

import pygame
from pygame.locals import *

import time

SIZE = 50
SURFACE = (0, 0, 0)
SPEED = 0.2


class apple:
    def __init__(self, screen):
        self.apple = pygame.image.load("resources/texture/apple.jpg").convert()
        self.screen = screen
        self.x = self.y = SIZE*3

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()


class cherry(apple):
    def __init__(self, screen):
        super().__init__(screen)
        self.cherry = pygame.image.load("resources/texture/cherry.jpg").convert()


class banana(apple):
    def __init__(self, screen):
        super().__init__(screen)
        self.banana = pygame.image.load("resources/texture/banana.jpg.jpg").convert()


class fig(apple):
    def __init__(self, screen):
        super().__init__(screen)
        self.fig = pygame.image.load("resources/texture/fig.jpg").convert()


class snake:
    def __init__(self, screen, length, direc):
        self.snake_img = pygame.image.load("resources/texture/snake.jpg").convert()
        self.length = length
        self.screen = screen
        self.direc = direc
        self.x = self.y = [SIZE]*length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.screen.fill(SURFACE)
        for i in range(self.length):
            self.screen.blit(self.snake_img, (self.x, self.y))
            pygame.display.flip()

    def move(self, direc):
        if direc == 'up' and self.direc != 'down':
            self.direc = 'up'
        if direc == 'down' and self.direc != 'up':
            self.direc = 'down'
        if direc == 'left' and self.direc != 'right':
            self.direc = 'left'
        if direc == 'right' and self.direc != 'left':
            self.direc = 'right'

    def slither(self):
        # The body will move one block behind the head -> backward loop
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        # The head
        if self.direc == 'left':
            self.x[0] -= SIZE
        if self.direc == 'right':
            self.x[0] += SIZE
        if self.direc == 'up':
            self.y[0] -= SIZE
        if self.direc == 'down':
            self.y[0] += SIZE
        self.draw()


def is_collision(x1, y1, x2, y2):  # (x1,y1) is apple cord. & (x2,y2) is the snake cord.
    if x2 <= x1 < x2 + SIZE:
        if y2 <= y1 < y2 + SIZE:
            return True
        return False


class game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(1000, 1000)
        self.surface.fill(SURFACE)
        pygame.display.set_caption("Simple Snake")
        pygame.display.flip()

        self.snake = snake(self.surface, 1, 'down')
        self.apple = apple(self.surface)
        self.cherry = cherry(self.surface)
        self.banana = banana(self.surface)
        self.fig = fig(self.surface)

        self.snake.draw()
        self.apple.draw()

    def game_over(self):
        self.surface.fill(SURFACE)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press ENTER, or to exit press ESCAPE", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def score_count(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.surface.fill(SURFACE)
        self.snake = snake(self.surface, 1, 'down')
        self.apple = apple(self.surface)

    def spawn(self, r):
        x = random.randint(0, 19) * SIZE
        y = random.randint(0, 19) * SIZE
        for i in range(self.snake.length):
            while x == self.snake.x[i] and y == self.snake.y[i]:
                x = random.randint(0, 19) * SIZE
                y = random.randint(0, 19) * SIZE
        if r == 0:
            self.cherry.set_coordinates(x, y)
            self.cherry.draw()
        elif r == 1:
            self.banana.set_coordinates(x, y)
            self.banana.draw()
        elif r == 2:
            self.fig.set_coordinates(x, y)
            self.fig.draw()
        else:
            self.apple.set_coordinates(x, y)
            self.apple.draw()

    def play(self):
        self.snake.slither()
        self.apple.draw()
        self.score_count()
        pygame.display.flip()

        # collision with apple
        if is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.spawn(10)
            self.snake.increase_length()

        # collision with body
        for i in range(3, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occurred"

    def run(self):
        FRUITS = pygame.USEREVENT+1
        pygame.time.set_timer(FRUITS, 3000)
        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if event.key == K_UP:
                        self.snake.move('up')
                    if event.key == K_DOWN:
                        self.snake.move('down')
                    if event.key == K_LEFT:
                        self.snake.move('left')
                    if event.key == K_RIGHT:
                        self.snake.move('right')
                if event.type == FRUITS:
                    r = random.randint(0, 2)
                    self.spawn(r)
                if event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(SPEED)


if __name__ == '__test__':
    game = game()
    game.run()
