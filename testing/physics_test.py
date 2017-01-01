import pygame
import sys

pygame.init()
game_screen = pygame.display.set_mode((1200, 800))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
