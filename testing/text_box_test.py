import sys
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1200, 800))


class TextBox():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def display(self):
        self.box_fill = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.box_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def on_hover(self):
        self.box_fill = pygame.draw.rect(screen, (67, 190, 187), (self.x, self.y, self.w, self.h))

    def on_click(self):
        self.box_fill = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))



txtbox1 = TextBox(600, 400, 300, 200)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
    txtbox1.display()
    pygame.display.update()
