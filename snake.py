import pygame

class Snake:
    """
    The body of the Snake
    """

    bg = (50, 153, 213)
    colorBody = (117, 134, 144)
    colorHead = (71, 77, 81)

    def __init__(self, window):
        self.window = window
        self.body = []
        # Añade cabeza
        self.body.append((window.widthInBlocks // 2, window.heightInBlocks // 2 + 1))
        # Añade 2 bloques de cuerpo
        self.body.append((window.widthInBlocks // 2, window.heightInBlocks // 2 + 2))
        self.body.append((window.widthInBlocks // 2, window.heightInBlocks // 2 + 3))
        self.dir = 0
        self.changeX = 0
        self.changeY = 0

    def drawSnake(self):
        for i in range(len(self.body)):
            block = self.body[len(self.body) - i - 1]
            if i == len(self.body) - 1:
                # Dibuja cabeza
                pygame.draw.rect(
                    self.window.window,
                    Snake.colorHead,
                    (
                        self.body[0][0] * self.window.blockSize,
                        self.body[0][1] * self.window.blockSize,
                        self.window.blockSize,
                        self.window.blockSize,
                    ),
                )
            else:
                # Dibuja cuerpo
                pygame.draw.rect(
                    self.window.window,
                    Snake.colorBody,
                    (
                        block[0] * self.window.blockSize,
                        block[1] * self.window.blockSize,
                        self.window.blockSize,
                        self.window.blockSize,
                    ),
                )

    def changeDirection(self, key):
        if key == 1 and self.dir != -1:
            self.dir = 1
            self.changeX = 0
            self.changeY = -1
        if key == 2 and self.dir != -2:
            self.dir = 2
            self.changeX = 1
            self.changeY = 0
        if key == -1 and self.dir != 1:
            self.dir = -1
            self.changeX = 0
            self.changeY = 1
        if key == -2 and self.dir != 2:
            self.dir = -2
            self.changeX = -1
            self.changeY = 0

    def move(self):
        self.body.pop()
        self.body.insert(0, (self.body[0][0] + self.changeX, self.body[0][1] + self.changeY))

    def eat(self):
        self.body.insert(0, (self.body[0][0] + self.changeX, self.body[0][1] + self.changeY))
