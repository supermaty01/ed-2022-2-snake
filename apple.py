import pygame
import random

class Apple:
    red = (213, 50, 80)

    def __init__(self, window, snake):
        self.appear = random.randint(0, 9)
        self.window = window
        self.snake = snake
        self.x = -1
        self.y = -1

    def drawApple(self):
        if self.appear != 0:
            self.appear -= 1
            return

        if self.x == -1:
            self.calPosition()

        pygame.draw.rect(
            self.window.window,
            Apple.red,
            (
                self.x * self.window.blockSize,
                self.y * self.window.blockSize,
                self.window.blockSize,
                self.window.blockSize,
            ),
        )

    def start(self):
        self.appear = 0
        self.x = self.snake.body[0][0] + 3
        self.y = self.snake.body[0][1] - 4

    def calPosition(self):
        self.x = random.randint(0, self.window.widthInBlocks - 1)
        self.y = random.randint(0, self.window.heightInBlocks - 1)

        while True:
            for block in self.snake.body:
                if block[0] == self.x and block[1] == self.y:
                    self.x = random.randint(0, self.window.widthInBlocks - 1)
                    self.y = random.randint(0, self.window.heightInBlocks - 1)

                    break
            break
