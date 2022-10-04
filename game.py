import pygame

class Game:
    bg = (194, 223, 227)
    colorScore = (37, 50, 55)
    colorLost = (37, 50, 55)
    colorGrid = (117, 134, 144)

    def __init__(self, widthInBlocks, heightInBlocks, blockSize):
        self.widthInBlocks = widthInBlocks
        self.heightInBlocks = heightInBlocks
        self.blockSize = blockSize
        self.window = pygame.display.set_mode(
            (self.widthInBlocks * self.blockSize, self.heightInBlocks * self.blockSize)
        )
        pygame.display.set_caption("ED - Snake")

    def setBackground(self):
        self.window.fill(Game.bg)

    def setGrid(self):
        # Horizontales
        for i in range(0, self.widthInBlocks):
            pygame.draw.line(
                self.window,
                self.colorGrid,
                (0, i * self.blockSize),
                (self.widthInBlocks * self.blockSize, i * self.blockSize),
            )
        # Verticales
        for i in range(0, self.heightInBlocks):
            pygame.draw.line(
                self.window,
                self.colorGrid,
                (i * self.blockSize, 0),
                (i * self.blockSize, self.heightInBlocks * self.blockSize),
            )

    def setScore(self, score):
        value = pygame.font.SysFont("bahnschrift", 35).render(
            "SCORE: " + str(score), True, Game.colorScore
        )
        self.window.blit(value, [5, 5])

    def setMessage(self, msg):
        mesg = pygame.font.SysFont("bahnschrift", 25).render(msg, True, Game.colorLost)
        mesg_rect = mesg.get_rect(
            center=(
                (self.widthInBlocks * self.blockSize) / 2,
                (self.heightInBlocks * self.blockSize) / 2,
            )
        )
        self.window.blit(mesg, mesg_rect)

    def instructions(self):
        lines = [
            "Use the arrow keys to move the snake.",
            "Eat food to grow. Stay on the board!",
            "And don't crash into yourself!",
            "",
            "",
            "To start, please press spacebar key",
        ]
        for i, l in enumerate(lines):
            mesg = pygame.font.SysFont("bahnschrift", 25).render(
                l, True, Game.colorLost
            )
            mesg_rect = mesg.get_rect(
                center=(
                    (self.widthInBlocks * self.blockSize) / 2,
                    (self.heightInBlocks * self.blockSize) / 2 - 2 * self.blockSize + 25 * i,
                )
            )
            self.window.blit(mesg, mesg_rect)
