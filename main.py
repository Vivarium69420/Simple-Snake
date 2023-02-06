import random
import time

import pygame
from pygame.locals import *

SIZE = 50
SURFACE = (22, 15, 45)
DELAY = 0.2


class Food:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/texture/Food.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        # The window size is (1000, 500)/50 = (20, 10) and given we count from 0 -> (20-1, 10-1) = (19,9) positions
        self.x = random.randint(0, 19)*SIZE
        self.y = random.randint(0, 9)*SIZE


class Snake:
    def __init__(self, parent_screen, length, direction):
        self.direction = direction
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/texture/block.jpg").convert()
        self.x = [SIZE]*length  # create an array with the length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        # increase the supposed length, and add another element into the array of both x and y
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(SURFACE)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move(self, direc):
        if direc == 'up' and self.direction != 'down':
            self.direction = 'up'
        if direc == 'down' and self.direction != 'up':
            self.direction = 'down'
        if direc == 'left' and self.direction != 'right':
            self.direction = 'left'
        if direc == 'right' and self.direction != 'left':
            self.direction = 'right'

    def slither(self):
        # The body will move one block behind the head -> backward loop
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        # The head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


def is_collision(x1, y1, x2, y2):  # (x1,y1) is apple cord. & (x2,y2) is the snake cord.
    if x2 <= x1 < x2 + SIZE:
        if y2 <= y1 < y2 + SIZE:
            return True
    return False


class Game:
    def __init__(self):
        # remember to init
        pygame.init()  # turn all of pygame on.
        self.surface = pygame.display.set_mode((1000, 500))
        self.surface.fill(SURFACE)
        self.snake = Snake(self.surface, 1, 'down')
        self.food = Food(self.surface)
        # The two draw of snake and food are different, since one is an arr, but the other is just an int
        self.snake.draw()
        self.food.draw()

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
        self.snake = Snake(self.surface, 1, 'down')
        self.food = Food(self.surface)

    def play(self):
        self.snake.slither()
        self.food.draw()  # apple need to draw or else it will be clear by slither
        self.score_count()
        pygame.display.flip()

        # collision with apple
        if is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.move()
            for i in range(self.snake.length):
                while self.food.x == self.snake.x[i] and self.food.y == self.snake.y[i]:
                    self.food.move()
            self.snake.increase_length()

        # collision with body
        for i in range(3, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occurred"  # to raise an exception

    def run(self):
        pause = False
        running = True
        while running:  # Loop for interactive UI
            for event in pygame.event.get():  # Read event doc for pygame
                if event.type == KEYDOWN:  # pressing a key
                    if event.key == K_ESCAPE:  # esc
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move('up')
                        if event.key == K_DOWN:
                            self.snake.move('down')
                        if event.key == K_LEFT:
                            self.snake.move('left')
                        if event.key == K_RIGHT:
                            self.snake.move('right')

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(DELAY)


if __name__ == '__main__':
    game = Game()
    game.run()
