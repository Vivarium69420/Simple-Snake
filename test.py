import random

import pygame
from pygame.locals import *

pygame.init()
SIZE = 50
window = pygame.display.set_mode((1200, 650))
bg = pygame.image.load('resources/texture/bg.jpg')
clock = pygame.time.Clock()


class Apple:
    def __init__(self):
        self.image = pygame.image.load("resources/texture/apple.jpg").convert()
        self.x = 500
        self.y = 500
        self.isSpeedBoosted = False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def set_coordinate(self, x1, y1):
        self.x = x1
        self.y = y1

    def move(self):
        x2 = random.randint(0, 23) * SIZE
        y2 = random.randint(0, 12) * SIZE
        self.x = x2
        self.y = y2


class Cherry(Apple):
    img = pygame.image.load('resources/texture/cherry.jpg')

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Fig(Apple):
    img = pygame.image.load('resources/texture/fig.jpg')

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Banana(Apple):
    img = pygame.image.load('resources/texture/banana.jpg')

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Snake:
    def __init__(self, direction, length):
        self.img = pygame.image.load('resources/texture/snake.jpg')
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = direction

    def draw(self, win):
        for body in range(self.length):
            win.blit(self.img, (self.x[body], self.y[body]))
        pygame.display.update()

    def move(self, direc):
        if direc == 'up' and self.direction != 'down':
            self.direction = 'up'
        if direc == 'down' and self.direction != 'up':
            self.direction = 'down'
        if direc == 'left' and self.direction != 'right':
            self.direction = 'left'
        if direc == 'right' and self.direction != 'left':
            self.direction = 'right'

    def slither(self, win):
        # The body will move one block behind the head -> backward loop
        for body in range(self.length - 1, 0, -1):
            self.x[body] = self.x[body - 1]
            self.y[body] = self.y[body - 1]
        # The head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw(win)

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


def is_collision(x1, y1, x3, y3):  # (x1,y1) is apple cord. & (x2,y2) is the snake cord.
    if x1 == x3 and y1 == y3:
        return True
    return False


def redraw_window():
    window.blit(bg, (0, 0))
    snake.slither(window)
    apple.draw(window)
    pygame.display.update()


pygame.time.set_timer(USEREVENT+1, 500)
apple = Apple()
snake = Snake('down', 50)
speed = 10
running = True
while running:
    # Apple
    if apple.isSpeedBoosted:
        speed = 25
    else:
        print('hello')
        speed = 10
        apple.isSpeedBoosted = False
    for i in range(snake.length):
        if is_collision(snake.x[0], snake.y[0], apple.x, apple.y):
            apple.move()
            if apple.x == snake.x[i] and apple.y == snake.y[i]:
                apple.move()
            snake.increase_length()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # esc
                running = False
            if event.key == K_RETURN:
                pause = False
            if event.key == K_UP:
                snake.move('up')
            if event.key == K_DOWN:
                snake.move('down')
            if event.key == K_LEFT:
                snake.move('left')
            if event.key == K_RIGHT:
                snake.move('right')
        if event.type == USEREVENT+1:
            apple.isSpeedBoosted = True
        if event.type == USEREVENT+2:
            apple.isSpeedBoosted = False

    redraw_window()
    clock.tick(speed)
pygame.quit()
