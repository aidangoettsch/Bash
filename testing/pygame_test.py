import sys
import pygame, pygame.gfxdraw
from pygame.locals import *

pygame.init()

screen_w = 1200
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
circle_x_inc = 2
circle_x = 400
circle = pygame.gfxdraw.aacircle(screen, circle_x, 400, 10, (255, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 255, 135))

    if circle_x >= screen_w or circle_x < 0: circle_x_inc *= -1

    circle_x *= circle_x_inc

    pygame.gfxdraw.aacircle(screen, circle_x, 400, 50, (255, 0, 0))
    pygame.gfxdraw.filled_circle(screen, circle_x, 400, 50, (255, 0, 0))

    clock.tick(60)
    pygame.display.update()
    print(circle_x_inc)
    # print(clock.get_fps())
