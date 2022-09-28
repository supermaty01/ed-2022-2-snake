import pygame
import random
from collections import deque


class Game:
    '''
    The game window and the functions associated with it
    '''

    bg = (194, 223, 227)
    colorScore = (37, 50, 55)
    colorLost = (37, 50, 55)

    def __init__(self, cantWidth, cantHeight, tamBlock):
        self.cantWidth = cantWidth
        self.cantHeight = cantHeight
        self.tamBlock = tamBlock
        self.window = pygame.display.set_mode((self.cantWidth*self.tamBlock, self.cantHeight*self.tamBlock))
        pygame.display.set_caption("ED - Snake")
    
    def setBackground(self):
        ''' Revisar '''
        self.window.fill(Game.bg)

    def Your_score(self, score):
        value = pygame.font.SysFont("bahnschrift", 35).render("SCORE: " + str(score), True, Game.colorScore)
        self.window.blit(value, [5, 5])

    def message(self, msg):
        mesg = pygame.font.SysFont("bahnschrift", 25).render(msg, True, Game.colorLost)
        mesg_rect = mesg.get_rect(center=((self.cantWidth*self.tamBlock)/2, (self.cantHeight*self.tamBlock)/2))
        self.window.blit(mesg, mesg_rect)

    def instructions(self):
        lines = ["Use the arrow keys to move the snake.", "Eat food to grow. Stay on the board!", "And don't crash into yourself!",'','' ,"To start, please press any arrow key"]
        for i, l in enumerate(lines):
            mesg = pygame.font.SysFont("bahnschrift", 25).render(l, True, Game.colorLost)
            mesg_rect = mesg.get_rect(center=((self.cantWidth*self.tamBlock)/2, (self.cantHeight*self.tamBlock)/2 - 2*self.tamBlock + 25*i))
            self.window.blit(mesg, mesg_rect)

class Snake:
    '''
    The body of the Snake
    '''
    bg = (50, 153, 213)
    colorBody = (117, 134, 144)
    colorHead = (71, 77, 81)

    def __init__(self, window: Game):
        self.window: Game = window
        self.body = deque()
        self.body.append((window.cantWidth//2, window.cantHeight//2))
        self.dir = 0
        self.changeX = 0
        self.changeY = 0

    def drawSnake(self):
        x = 0
        pygame.draw.rect(self.window.window, Snake.colorHead, (self.body[0][0]*self.window.tamBlock, self.body[0][1]*self.window.tamBlock, self.window.tamBlock, self.window.tamBlock))
        for block in self.body:
            if x == 0:
                x += 1
                continue

            pygame.draw.rect(self.window.window, Snake.colorBody, (block[0]*self.window.tamBlock, block[1]*self.window.tamBlock, self.window.tamBlock, self.window.tamBlock))
        

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
        if len(self.body) == 1:
            block = self.body.pop()
            self.body.appendleft((block[0]+self.changeX, block[1]+self.changeY))
        else:
            self.body.pop()
            self.body.appendleft((self.body[0][0]+self.changeX, self.body[0][1]+self.changeY))

    def eat(self):
        self.body.appendleft((self.body[0][0]+self.changeX, self.body[0][1]+self.changeY))


class Apple:
    red = (213, 50, 80)

    def __init__(self, window: Game, snake: Snake):
        self.appear = random.randint(0,9)
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

        pygame.draw.rect(self.window.window, Apple.red, (self.x*self.window.tamBlock, self.y*self.window.tamBlock, self.window.tamBlock, self.window.tamBlock))

    def inicio(self):
        self.appear = 0
        self.x = self.snake.body[0][0]+3
        self.y = self.snake.body[0][1]-3

    def calPosition(self):
        self.x = random.randint(0, self.window.cantWidth-1)
        self.y = random.randint(0, self.window.cantHeight-1)

        while True:
            x = True
            y = True

            for block in self.snake.body:
                if block[0] == self.x:
                    self.x = random.randint(0, self.window.cantWidth-1)
                    x = False
                    break

            for block in self.snake.body:
                if block[1] == self.y:
                    self.y = random.randint(0, self.window.cantHeight-1)
                    y = False
                    break

            if not (x == False and y == False):
                break

        



def gameLopp():
    pygame.init()
    window = Game(31,25,30)
    snake = Snake(window)
    apple = Apple(window, snake)
    apple.inicio()
    gameClose = False
    gameOver = False

    while not gameClose:
        
        # Player loses
        while gameOver:
            window.setBackground()
            window.message("You have lost. Please enter 'C' to play again")
            window.Your_score(len(snake.body) - 1)
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
            if event.type == pygame.KEYDOWN:
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

        if snake.dir == 0:
            window.setBackground()
            window.instructions()
            pygame.display.update()
            continue


        window.setBackground()

        x = snake.body[0][0]
        y = snake.body[0][1]

        if x >= window.cantWidth or x < 0 or y >= window.cantHeight or y < 0:
            gameOver = True
            continue
        
        i = 1
        for block in snake.body:
            if i == 1:
                i += 1
                continue

            if x == block[0] and y == block[1]:
                gameOver = True
                break
        
        if gameOver:
            continue

        if snake.body[0][0] == apple.x and snake.body[0][1] == apple.y:
            apple = Apple(window, snake)
            snake.eat()
        else:
            snake.move()

        apple.drawApple()
        snake.drawSnake()

        window.Your_score(len(snake.body) - 1)

        pygame.display.update()

        pygame.time.delay(100)
               
    pygame.quit()

if __name__ == '__main__':
    gameLopp()