import pygame
import random
from collections import deque

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
dark_grey = (45, 45, 45)
light_grey = (130, 130, 130)
red = (213, 50, 80)
blue = (50, 153, 213)


# Tamaño de pantalla de 13x32 + 10
# 13 Cuadriculas
# 30 px tamaño de cuadricula
# 5 px de margen a cada lado
margin = 5
dis_width = 400
dis_height = 400


dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("ED - Snake")

clock = pygame.time.Clock()

snake_block = 30
snake_speed = 3

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 35)


def Your_score(score):
    value = score_font.render("SCORE: " + str(score), True, yellow)
    dis.blit(value, [5, 5])


def our_snake(snake_block, snake_list):
    for x in range(0, len(snake_list) - 1):
        pygame.draw.rect(
            dis,
            light_grey,
            [snake_list[x][0], snake_list[x][1], snake_block, snake_block],
        )
    pygame.draw.rect(
        dis, dark_grey, [snake_list[-1][0], snake_list[-1][1], snake_block, snake_block]
    )


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def setBackground():
    dis.fill(blue)
    pygame.draw.rect(dis, black, [0, 0, 5, 400])
    pygame.draw.rect(dis, black, [0, 0, 400, 5])
    pygame.draw.rect(dis, black, [395, 0, 400, 400])
    pygame.draw.rect(dis, black, [0, 395, 400, 400])


def gameLoop():
    game_over = False
    game_close = False

    # Inicia en una posicion central (6ta casilla)
    x1 = margin + 6 * snake_block
    y1 = margin + 6 * snake_block

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, 13)) * snake_block + margin
    foody = round(random.randrange(0, 13)) * snake_block + margin

    while not game_over:

        while game_close == True:
            setBackground()
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 > dis_width - snake_block - 5 or x1 < 5 or y1 > dis_height - snake_block - 5 or y1 < 5:
            game_close = True
            continue
        x1 += x1_change
        y1 += y1_change
        setBackground()
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        print(snake_List)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, 13)) * 30 + margin
            foody = round(random.randrange(0, 13)) * 30 + margin
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()