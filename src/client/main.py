# import asyncio
# import websockets
import os
import sys
import pygame
import pygame.freetype

# Initialize and check pygame initialization
try:
    pygame.init()
except:
    print("Pygame initialization failed. Check your game installation.")
    sys.exit()

# Variable Declarations
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
menu_font = pygame.freetype.Font('src/client/resources/Slabo_REG.ttf', 27)
state = "MENU"

# Core Functions
def render_menu():
    """
    Renders the menu screen

    :return:
    """
    # Background color
    screen.fill(pygame.Color(0, 150, 136))

    # Button - Main Server
    menu_button_1 = Menu_Button("Main Server", 350, 200, 500, 80)
    menu_button_1 = Menu_Button("Main Server", 350, 200, 500, 80)
    menu_button_1 = Menu_Button("Main Server", 350, 200, 500, 80)
    menu_button_1 = Menu_Button("Main Server", 350, 200, 500, 80)

def blit_text(text, x, y):
    """
    Blits text to the screen

    :return:
    """
    text_surface = menu_font.render(text, (0, 0, 0), (0, 0, 0))
    screen.blit(text_surface, text_surface.get_rect())

def reset():
    """
    Reset the game state after exiting from a game or when starting the game.

    Renders the portions of the client that are out of the game, such as the menu.
    :return:
    """
    global state

    state = "MENU"
    while True:
        # Clear screen
        if state == 'MENU':
            render_menu()
        else:
            break

# Classes
class Menu_Button():
    """
    Represents a menu button

    :return:
    """

    def __init__(self, text, x, y, w, h):
        self.text          = text
        self.x             = x
        self.y             = y
        self.w             = w
        self.h             = h
        self.topl_loc      = (x, y)
        self.botr_loc      = (x + w, y + h)
        self.button_text   = blit_text(text, x, y)
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (x, y, w, h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h), 2)

    # def on_hover(self, callback()):

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    render_menu()
    pygame.display.update()
    clock.tick(60)
    print("FPS > " + str(clock.get_fps()))

# async def frame():
#     async with websockets.connect('ws://localhost:8765') as websocket:
#
#         name = input("What's your name? ")
#         await websocket.send(name)
#         print("> {}".format(name))
#
#         greeting = await websocket.recv()
#         print("< {}".format(greeting))
#
# asyncio.get_event_loop().run_until_complete(hello())
#
# # Connect
# socket = websockets.connect('ws://localhost:8080')
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# reset()
