import sys
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1200, 800))
font = pygame.font.SysFont("comicsans", 72)
font_surface = font.render("Hello World!", True, (0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
    screen.fill((255, 255, 255))
    screen.blit(font_surface, (100, 100))

    pygame.display.update()
