import pygame

pygame.init()
dis=pygame.display.set_mode((500,500))
pygame.display.update()

gameOver = False
while not gameOver:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            gameOver = True

pygame.quit()
