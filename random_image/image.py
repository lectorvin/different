import random
import pygame
from pygame import *


running = 1
screenWidth, screenHeight = 100, 100
pygame.init()
pygame.display.set_caption('Image')
screen = pygame.display.set_mode((screenWidth, screenHeight))


def draw():
    for row in range(screenHeight):
        for col in range(screenWidth):
            pf = pygame.Surface((1, 1))
            pf.fill((
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255)))
            screen.blit(pf, (col, row))


while running:
    draw()
    pygame.display.flip()
    pygame.time.delay(1000)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

pygame.display.quit()
