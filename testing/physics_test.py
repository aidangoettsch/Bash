import sys
sys.path.append('..')
import pygame
from pygame.locals import *
from src.common.player import Player

pygame.init()
game_screen = pygame.display.set_mode((1200, 800))
player_1_player = Player("Player 1")
player_1 = pygame.

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
