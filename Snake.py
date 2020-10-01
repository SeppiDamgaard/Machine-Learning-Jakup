
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import TensorBoard
from keras.models import load_model
from keras import optimizers
import numpy as np
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from pathlib import Path
import pygame
import time
import random
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)
freshModel = True
trainingData = []
numberOfGames = 20
epochs = 60
output = 0

moveLimit = 200

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

disHeight = 400
disWidth = 400
centerWidth = disWidth /2
centerHeight = disHeight / 2

clock = pygame.time.Clock()

dis=pygame.display.set_mode((disWidth,disHeight))
pygame.display.set_caption('Machine Learning: Snake')

snakeBlock = 10
snakeSpeed = 30000

my_file = Path("gamemodel.h5")
if my_file.is_file():
    # Henter allerede trænet model  
    model = load_model('gamemodel.h5')
    print('Model fundet')
    freshModel = False
else:
    # laver ny model om den ikke allerede eksisterer
    model = Sequential()
    model.add(Dense(32, input_dim=6, activation='sigmoid'))
    model.add(Dense(20, activation='sigmoid'))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(10, activation='sigmoid'))
    model.add(Dense(4, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])
    print('Ny model lavet, ingen model fundet...')

if freshModel:
    score_requirement = 1
else:
    score_requirement = 1

def ourSnake (snakeBlock, snakeList):
    for x in snakeList:
        pygame.draw.rect(dis, green, [x[0], x[1], snakeBlock, snakeBlock])

def ShowScore(score):
    scoreFont = pygame.font.SysFont("bahnschrift", 25)
    dis.blit(scoreFont.render("Score: " +str(score), True, white), [0,0])

def message(msg, clr):
    fontStyle = pygame.font.SysFont("bahnschrift", 30)  
    mesg = fontStyle.render(msg, True, clr)
    dis.blit(mesg, [disWidth/6.0, disHeight/3.0])


def gameLoop():    
    global moveLimit
    #Define the windows itself
    pygame.init()
    

    gameOver = False
    gameClose = False
    keyUp = False
    
    gameMemory = []

    x = centerWidth
    y = centerHeight

    x_change = 0
    y_change = 0

    snakeList = []
    snakeLenght = 1
    snakeHead = [centerWidth, centerHeight]
    global count
    count = 0

    foodx = round(random.randrange(0, disWidth - snakeBlock) / 10.0) * 10.0
    foody = round(random.randrange(0, disHeight - snakeBlock) / 10.0) * 10.0
    #print("Foodx: " + str(foodx) + "\nFoody: " + str(foody))

    while count <= moveLimit:
        count += 1
        if gameOver or gameClose:
            break

        inputData = [snakeHead[0] / disWidth, snakeHead[1] / disHeight, foodx / disWidth, foody/ disHeight, 1, 1]
        if freshModel:
            output = random.randint(0, 3)
        else:
            outputData = model.predict([inputData])[0].tolist()
            output = outputData.index(max(outputData))
        desiredOutput = None

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYUP or event.type == pygame.MOUSEMOTION:
                keyUp = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_END:
                    print('YEED')
                    pygame.quit()
                    quit()
    
        if output == 0:
            x_change = -snakeBlock
            y_change = 0
            lastKeyPressed = pygame.K_LEFT
            desiredOutput = [1, 0, 0, 0]
        elif output == 1:
            x_change = snakeBlock
            y_change = 0
            lastKeyPressed = pygame.K_RIGHT
            desiredOutput = [0, 1, 0, 0]
        elif output == 2:
            x_change = 0
            y_change = -snakeBlock
            lastKeyPressed = pygame.K_UP
            desiredOutput = [0, 0, 1, 0]
        elif output == 3:
            x_change = 0
            lastKeyPressed = pygame.K_DOWN
            y_change = snakeBlock
            desiredOutput = [0, 0, 0, 1]

        gameMemory.append([inputData, desiredOutput])

        if keyUp:
            #print('continue')
            continue
        if x >= disWidth or x < 0 or y >= disHeight or y < 0:
            # print('Reached border')
            break
        #print("\nx: " + str(x) + "\ny" + str(y))
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
                print('here?')
                gameOver = True
        ourSnake(snakeBlock, snakeList)
        ShowScore(snakeLenght - 1)
        pygame.draw.rect(dis,green,[x,y,snakeBlock,snakeBlock])
        pygame.display.update()
        if x == foodx and y == foody:
            snakeLenght += 1
            moveLimit += 200
            foodSpawned = False
            if snakeLenght == ((disHeight / 10) * (disWidth / 10)):
                gameClose = True
            while not foodSpawned:
                foodx = round(random.randrange(0, disWidth - snakeBlock) / 10.0) * 10.0
                foody = round(random.randrange(0, disHeight - snakeBlock) / 10.0) * 10.0
                for i in snakeList:
                    if not (foodx == i[0] and foody == i[0]):
                        foodSpawned = True
                        # x_change = 0
                        # y_change = 0
                        break

    if snakeLenght - 1 >= score_requirement:
        print(gameMemory)
        for data in gameMemory[0:len(gameMemory) - 4]:
            trainingData.append([data[0], data[1]])
        # print(trainingData)
        # gameMemory = np.array(gameMemory)
        # xData = gameMemory[:,0]
        # yData = gameMemory[:,1]

        # xData = xData[0:int(len(xData) * 0.9)]
        # yData = yData[0:int(len(yData) * 0.9)]

        # trainingData.append([xData, yData])

    # pygame.quit()

def trainModel():
    tmp = np.array(trainingData)
    # print(tmp)
    x = tmp[:,0].tolist()
    y = tmp[:,1].tolist()



    model.fit(x,y,epochs=epochs, verbose=1)
    model.save('gamemodel.h5')


def play():
    global trainingData
    global moveLimit
    global freshModel
    global score_requirement
    trainDataHolder = []
    count = 0
    while True:
        moveLimit = 200
        gameLoop()

        if not trainingData == []:
            count += 1
            trainDataHolder += trainingData
            trainingData.clear()
            print(str(count))
        
        if freshModel:
            if count == 100:
                trainingData = trainDataHolder
                trainModel()
                freshModel = False
                score_requirement = 2
        elif count == 5 and freshModel == False:
            trainingData = trainDataHolder
            trainModel()
            count = 0

            



play()