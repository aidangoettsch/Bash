import sys
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1200, 800))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
