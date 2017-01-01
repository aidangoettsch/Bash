import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

circle_x = 400
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 255, 135))

    circle_x += 1
    pygame.draw.circle(screen, (255, 0, 0), (circle_x + 2, 400), 20)

    pygame.display.update()
    print(clock.get_fps())
