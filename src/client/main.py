# import asyncio
# import websockets
import os
import sys
import pygame
import pygame.freetype

# Initialize and check pygame initialization
try:
    pygame.init()
    pygame.freetype.init()
except:
    print("Pygame initialization failed. Check your game installation.")
    sys.exit()

# Variable Declarations
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
state = "MENU"
mouse = pygame.mouse
menu = {
    "font": pygame.freetype.Font('src/client/resources/Slabo_REG.ttf', 27),
    "buttons": []
}


# Core Functions
def render_menu():
    """
    Renders the menu screen

    :return:
    """
    # Declare globals
    global menu

    # Background color
    screen.fill(pygame.Color(0, 150, 136))

    # Main Menu Buttons
    menu["buttons"] = [
        Menu_Button("Main Server", 350, 200, 500, 80),
        Menu_Button("Custom Server", 350, 300, 500, 80),
        Menu_Button("Localhost", 350, 400, 500, 80),
        Menu_Button("Help", 350, 500, 500, 80)
    ]


def blit_text(text, x, y):
    """
    Blits text to the screen

    :return: Text surfaced with text rendered on it
    """
    global menu

    text_surface = menu["font"].render(text, (255, 255, 255))
    screen.blit(text_surface[0], (x, y))
    return text_surface


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

    def on_hover(self):
        self.button_fill   = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 2)

    def off_hover(self):
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 2)

    def hide_button(self):
        self.button_text   = None
        self.button_fill   = None
        self.button_border = None

    # def on_click(self):


def main():
    """
    This is the main game loop. Everything deviates from this function: Menus, the game itself, etc.

    * Returns nothing
    * Function completes when running becomes false
    """
    global mouse
    global state
    running = True

    while running:
        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Renders menu
        if state == "MENU":
            # Renders base menu
            render_menu()

            # Button handler for the menu
            for button in menu["buttons"]:
                if button.button_fill.collidepoint(mouse.get_pos()):
                    button.on_hover()

        # Updates screen and FPS clock
        pygame.display.update()
        clock.tick(60)
        print("FPS > " + str(clock.get_fps()))

# Runs the main loop, and exits the process when main terminates
main()
sys.exit()


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
