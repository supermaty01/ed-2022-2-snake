import pygame
from apple import Apple
from snake import Snake
from game import Game

def gameLoop():
    pygame.init()
    window = Game(13, 13, 45)
    snake = Snake(window)
    apple = Apple(window, snake)
    apple.start()
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
                        gameLoop()
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
        if x >= window.widthInBlocks or y < 0 or x < 0 or y >= window.heightInBlocks:
            gameOver = True
            continue

        apple.drawApple()
        snake.drawSnake()

        window.setScore(len(snake.body) - 3)

        pygame.display.update()

        pygame.time.delay(1000)

    pygame.quit()

if __name__ == "__main__":
    gameLoop()