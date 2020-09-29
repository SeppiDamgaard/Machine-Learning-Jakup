import pygame
import time
import random

pygame.init()

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

disHeight = 400
disWidth = 400
centerWidth = disWidth /2
centerHeight = disHeight / 2

clock = pygame.time.Clock()

#Define the windows itself
dis=pygame.display.set_mode((disWidth,disHeight))
pygame.display.set_caption('Machine Learning: Snake')


snakeBlock = 10
snakeSpeed = 30

fontStyle = pygame.font.SysFont("bahnschrift", 30)
scoreFont = pygame.font.SysFont("bahnschrift", 25)

def ourSnake (snakeBlock, snakeList):
    for x in snakeList:
        pygame.draw.rect(dis, green, [x[0], x[1], snakeBlock, snakeBlock])

def ShowScore(score):
    dis.blit(scoreFont.render("Score: " +str(score), True, white), [0,0])

def message(msg, clr):
    mesg = fontStyle.render(msg, True, clr)
    dis.blit(mesg, [disWidth/6, disHeight/3])

def gameLoop():    
    gameOver = False
    gameClose = False
    
    x = centerWidth
    y = centerHeight

    x_change = 0
    y_change = 0

    snakeList = []
    snakeLenght = 1

    foodx = round(random.randrange(0, disWidth - snakeBlock) / 10.0) * 10.0
    foody = round(random.randrange(0, disHeight - snakeBlock) / 10.0) * 10.0
    print("Foodx: " + str(foodx) + "\nFoody: " + str(foody))

    while not gameOver:

        while gameClose == True:
            dis.fill(white)
            message("You lost! Press Q to quit, or R to play again!", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameClose = False
                        gameOver = True
                    if event.key == pygame.K_r:
                        gameLoop()


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snakeBlock
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snakeBlock
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -snakeBlock
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = snakeBlock

            if x >= disWidth or x < 0 or y >= disHeight or y < 0:
                gameClose = True
            print("\nx: " + str(x) + "\ny" + str(y))
            x += x_change
            y += y_change
            dis.fill(black)
            pygame.draw.rect(dis, red, [foodx, foody, snakeBlock, snakeBlock])
            snakeHead = []
            snakeHead.append(x)
            snakeHead.append(y)
            snakeList.append(snakeHead)
            if len(snakeList) > snakeLenght:
                del snakeList[0]

            for i in snakeList[:-1]:
                if i == snakeHead:
                    gameClose = True

            ourSnake(snakeBlock, snakeList)
            ShowScore(snakeLenght - 1)

            pygame.draw.rect(dis,green,[x,y,snakeBlock,snakeBlock])
            pygame.display.update()

            if x == foodx and y == foody:
                foodx = round(random.randrange(0, disWidth - snakeBlock) / 10.0) * 10.0
                foody = round(random.randrange(0, disHeight - snakeBlock) / 10.0) * 10.0
                snakeLenght += 1

            clock.tick(30)
    pygame.quit()

gameLoop()