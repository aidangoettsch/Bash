import asyncio
import websockets
import os
import sys
import pygame
import json

# Initialize and check pygame initialization
try:
    pygame.init()
except:
    print("Pygame initialization failed. Check your game installation.")
    sys.exit()

# Variable Declarations
screen_w = 1200
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
state = "MENU"
mouse = pygame.mouse

shadow_overlay = pygame.Surface((1200, 800), pygame.SRCALPHA, 32)
shadow_overlay.fill((0, 0, 0, 0))
screen.blit(shadow_overlay, (0, 0))

menu = {
    "font": pygame.font.Font('src/client/resources/Slabo_REG.ttf', 27),
    "buttons": []
}

default_connection = {
    "ip": "lccnetwork.dynu.net",
    "port": 8080
}

connection = {}

events = {
    "MOUSEDOWN": False
}


# Core Functions
def render_menu():
    """
    Renders the menu screen

    :return:
    """
    # Declare globals
    global menu

    def on_click_connect_main():
        global state
        state = "CONNECTING_MAIN"

    def on_click_connect_custom():
        global state
        state = "MENU_CUSTOM"

    def on_click_connect_localhost():
        global state
        state = "CONNECTING_LOCALHOST"

    def on_click_show_help():
        global state
        state = "HELP"

    # Main Menu Buttons
    menu["buttons"] = [
        MenuButton("Main Server", 350, 200, 500, 80, on_click_connect_main),
        MenuButton("Custom Server", 350, 300, 500, 80, on_click_connect_custom),
        MenuButton("Localhost", 350, 400, 500, 80, on_click_connect_localhost),
        MenuButton("Help", 350, 500, 500, 80, on_click_show_help)
    ]


def fill_screen():
    """
    Fills the background of the screen based on the state variable

    """
    if state.startswith("MENU"):
        screen.fill((0, 150, 136))
    elif state.startswith("GAME"):
        screen.fill((0, 96, 100))


def blit_text(text, x, y):
    """
    Blits text to the screen

    :return:
    """
    global screen_h, screen_w

    text_surface = menu["font"].render(text, True, (0, 0, 0))
    screen.blit(text_surface, text_surface.get_rect(center=(x, y)))


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
class MenuButton():
    """
    Represents a menu button

    :return:
    """

    def __init__(self, text, x, y, w, h, on_click_function):
        self.text                   = text
        self.x                      = x
        self.y                      = y
        self.w                      = w
        self.h                      = h
        self.topl_loc               = (x, y)
        self.botr_loc               = (x + w, y + h)
        self.mid_loc                = (x + w / 2, y + h / 2)
        self.on_click_function      = on_click_function

    def display_button(self):
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def display_text(self):
        self.button_text   = blit_text(self.text, self.mid_loc[0], self.mid_loc[1])

    def on_hover(self):
        self.button_fill   = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def off_hover(self):
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def on_click(self):
        self.on_click_function()


def main():
    """
    This is the main game loop. Everything deviates from this function: Menus, the game itself, etc.

    * Returns nothing
    * Function completes when running becomes false
    """
    global state, shadow_overlay, events
    running = True

    while running:
        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                events["MOUSEDOWN"] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                events["MOUSEDOWN"] = False

        # Fills screen background
        fill_screen()

        # Renders menu base
        if state.startswith("MENU"):
            # Renders base menu
            render_menu()

            # Main Menu Screen
            if state == "MENU":
                for button in menu["buttons"]:
                    # Renders the button
                    button.display_button()

                    # Hover and Click handler
                    if button.button_fill.collidepoint(mouse.get_pos()):
                        button.on_hover()
                        if events["MOUSEDOWN"]:
                            button.on_click()
                    else:
                        button.off_hover()

                    # Renders the text
                    button.display_text()

        # Connecting screen handler
        if state.startswith("CONNECTING"):
            if state.startswith("CONNECTING_LOCALHOST"):
                connection["ip"] = "127.0.0.1"
                connection["port"] = 8080

                state = "INGAME"

        #
        if state.startswith("INGAME"):
            loop = asyncio.get_event_loop()
            loop.create_task(frame())
            loop.run_forever()

        # Updates screen and FPS clock
        pygame.display.update()
        clock.tick(60)
        # print("FPS > " + str(clock.get_fps()))
        print(state)

async def frame():
    async with websockets.connect("ws://" + connection["ip"] + ":" + str(connection["port"])) as websocket:
        join_packet = {
            "name": "testing"
        }
        await websocket.send(json.dumps(join_packet))

        player_id = json.loads(await websocket.recv())["player_id"]
        state = {}

        while True:
            state = json.loads(await websocket.recv())


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
