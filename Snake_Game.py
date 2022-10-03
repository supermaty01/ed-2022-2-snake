import pygame
import random


class Game:
    """
    The game window and the functions associated with it
    """

    bg = (194, 223, 227)
    colorScore = (37, 50, 55)
    colorLost = (37, 50, 55)
    colorGrid = (117, 134, 144)

    def __init__(self, blocksWidth, blocksHeight, tamBlock):
        self.blocksWidth = blocksWidth
        self.blocksHeight = blocksHeight
        self.tamBlock = tamBlock
        self.window = pygame.display.set_mode(
            (self.blocksWidth * self.tamBlock, self.blocksHeight * self.tamBlock)
        )
        pygame.display.set_caption("ED - Snake")

    def setBackground(self):
        self.window.fill(Game.bg)

    def setGrid(self):
        # Horizontales
        for i in range(0, self.blocksWidth):
            pygame.draw.line(
                self.window,
                self.colorGrid,
                (0, i * self.tamBlock),
                (self.blocksWidth * self.tamBlock, i * self.tamBlock),
            )
        # Verticales
        for i in range(0, self.blocksHeight):
            pygame.draw.line(
                self.window,
                self.colorGrid,
                (i * self.tamBlock, 0),
                (i * self.tamBlock, self.blocksHeight * self.tamBlock),
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
                (self.blocksWidth * self.tamBlock) / 2,
                (self.blocksHeight * self.tamBlock) / 2,
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
                    (self.blocksWidth * self.tamBlock) / 2,
                    (self.blocksHeight * self.tamBlock) / 2 - 2 * self.tamBlock + 25 * i,
                )
            )
            self.window.blit(mesg, mesg_rect)


class Snake:
    """
    The body of the Snake
    """

    bg = (50, 153, 213)
    colorBody = (117, 134, 144)
    colorHead = (71, 77, 81)

    def __init__(self, window: Game):
        self.window: Game = window
        self.body = []
        # Añade cabeza
        self.body.append((window.blocksWidth // 2, window.blocksHeight // 2 + 1))
        # Añade 2 bloques de cuerpo
        self.body.append((window.blocksWidth // 2, window.blocksHeight // 2 + 2))
        self.body.append((window.blocksWidth // 2, window.blocksHeight // 2 + 3))
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
                        self.body[0][0] * self.window.tamBlock,
                        self.body[0][1] * self.window.tamBlock,
                        self.window.tamBlock,
                        self.window.tamBlock,
                    ),
                )
            else:
                # Dibuja cuerpo
                pygame.draw.rect(
                    self.window.window,
                    Snake.colorBody,
                    (
                        block[0] * self.window.tamBlock,
                        block[1] * self.window.tamBlock,
                        self.window.tamBlock,
                        self.window.tamBlock,
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


class Apple:
    red = (213, 50, 80)

    def __init__(self, window: Game, snake: Snake):
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
                self.x * self.window.tamBlock,
                self.y * self.window.tamBlock,
                self.window.tamBlock,
                self.window.tamBlock,
            ),
        )

    def inicio(self):
        self.appear = 0
        self.x = self.snake.body[0][0] + 3
        self.y = self.snake.body[0][1] - 4

    def calPosition(self):
        self.x = random.randint(0, self.window.blocksWidth - 1)
        self.y = random.randint(0, self.window.blocksHeight - 1)

        while True:
            for block in self.snake.body:
                if block[0] == self.x and block[1] == self.y:
                    self.x = random.randint(0, self.window.blocksWidth - 1)
                    self.y = random.randint(0, self.window.blocksHeight - 1)

                    break
            break


def gameLopp():
    pygame.init()
    window = Game(13, 13, 45)
    snake = Snake(window)
    apple = Apple(window, snake)
    apple.inicio()
    gameClose = False
    gameOver = False
    instructionsSkipped = False

    while not gameClose:

        # Player loses
        while gameOver:
            window.setBackground()
            window.setMessage("You have lost. Please press 'C' key to play again")
            window.setScore(len(snake.body) - 3)
            pygame.display.update()

            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    gameClose = True
                    gameOver = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pygame.quit()
                        gameLopp()
                        return

        if gameClose:
            pygame.quit()
            break

        # Events
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                gameClose = True
                break

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and not instructionsSkipped
            ):
                snake.changeDirection(1)
                instructionsSkipped = True
                break
            if event.type == pygame.KEYDOWN and instructionsSkipped:
                if event.key == pygame.K_LEFT:
                    snake.changeDirection(-2)
                    break
                elif event.key == pygame.K_RIGHT:
                    snake.changeDirection(2)
                    break
                elif event.key == pygame.K_UP:
                    snake.changeDirection(1)
                    break
                elif event.key == pygame.K_DOWN:
                    snake.changeDirection(-1)
                    break

        if gameClose:
            pygame.quit()
            break

        if not instructionsSkipped:
            window.setBackground()
            window.instructions()
            pygame.display.update()
            continue

        window.setBackground()
        window.setGrid()

        if gameOver:
            continue

        if snake.body[0][0] == apple.x and snake.body[0][1] == apple.y:
            apple = Apple(window, snake)
            snake.eat()
        else:
            snake.move()

        # Revisa si se choca con su cuerpo
        x = snake.body[0][0]
        y = snake.body[0][1]
        for i in range(1, len(snake.body)):
            block = snake.body[i]
            if x == block[0] and y == block[1]:
                gameOver = True
                break
        # Revisa si se sale de la pantalla
        if x >= window.blocksWidth or y < 0 or x < 0 or y >= window.blocksHeight:
            gameOver = True
            continue

        apple.drawApple()
        snake.drawSnake()

        window.setScore(len(snake.body) - 3)

        pygame.display.update()

        pygame.time.delay(1000)

    pygame.quit()


if __name__ == "__main__":
    gameLopp()