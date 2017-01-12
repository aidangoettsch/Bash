import asyncio
import websockets
import os
import sys
import pygame
import pygame.freetype
import pygame.gfxdraw
import json
import time
import copy

# Initialize and check pygame initialization
try:
    pygame.init()
except:
    print("Pygame initialization failed. Check your game installation.")
    sys.exit()

# Sets the caption of the window
pygame.display.set_caption("BASH - Created by Aidan G. & Brian X.")

# Variable Declarations
screen_w = 1200
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
mouse = pygame.mouse
target_fps = 60.0
frame_interval = 1.0 / target_fps

loop = asyncio.get_event_loop()

# =======================================================
# States of the game
# This variable controls the client, and what it renders
# =======================================================
# MENU = Main menu screen
# CONNECTING_LOCALHOST = Connecting to localhost server
# CONNECTING_MAIN = Connecting to the main server
# INGAME = In the game
# =======================================================
state = "MENU"
start_time = time.time()

menu = {
    "font": pygame.freetype.Font('src/client/resources/Slabo_REG.ttf', 27),
    "buttons": [],
    "shadow": None
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
        state = "CONNECTING_CUSTOM"

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

    # Main Menu Shadow Overlay
    menu["shadow"] = Shadow()


def fill_screen():
    """
    Fills the background of the screen based on the state variable, and applies shadow if necessary

    """
    global menu, state

    if state.startswith("MENU"):
        screen.fill((0, 150, 136))
    if state.startswith("CONNECTING"):
        screen.fill((0, 96, 100))
        menu["shadow"].opacitize(120)
    if state.startswith("HELP"):
        screen.fill((0, 150, 136))
        menu["shadow"].opacitize(120)
    if state.startswith("INGAME"):
        screen.fill((0, 96, 100))


def blit_text(text, x, y, text_size, bold=False):
    """
    Blits text to the screen

    :return:
    """
    global menu

    if bold:
        text_surface = menu["font"].render(text, fgcolor=(0, 0, 0), style=pygame.freetype.STYLE_STRONG, size=text_size)
    else:
        text_surface = menu["font"].render(text, fgcolor=(0, 0, 0), size=text_size)

    screen.blit(text_surface[0], text_surface[0].get_rect(center=(x, y)))


def alpha_rect(loc, size, color, opacity):
    rect = pygame.Surface(size)
    rect.set_alpha(opacity)
    rect.fill(color)
    screen.blit(rect, loc)


def reset():
    """
    Reset the game state after exiting from a game or when starting the game.
    Renders the portions of the client that are out of the game, such as the menu.
    :return:
    """
    global state, loop

    state = "MENU"
    loop.stop()
    main()


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
        self.button_text   = blit_text(self.text, self.mid_loc[0], self.mid_loc[1], 32, bold=True)

    def on_hover(self):
        self.button_fill   = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def off_hover(self):
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def on_click(self):
        self.on_click_function()


class Shadow():
    """
    Represents a shadow backdrop behind everything

    """
    def __init__(self):
        self.opacity = 0
        self.shadow  = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)

    def inc_opacity(self, alpha):
        self.opacity += 1
        self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)
        if self.opacity >= alpha:
            return True
        else:
            return False

    def opacitize(self, alpha):
        self.opacity  = alpha
        self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)

    def deopacitize(self):
        self.opacity  = 0
        self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)

    def fade_in(self, opacity, duration):
        while self.opacity <= opacity:
            print(self.opacity, opacity)
            self.opacity += 2
            self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)
            pygame.display.update

    def fade_out(self, opacity):
        while self.opacity > opacity:
            self.opacity -= 5
            self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)


def main():
    """
    This is the main game loop. Everything deviates from this function: Menus, the game itself, etc.

    * Returns nothing
    """
    global state, shadow_overlay, events, loop

    while True:
        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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

                    # Renders our game title
                    blit_text("$bash_", 600, 100, 84, bold=True)

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
            if state == "CONNECTING_LOCALHOST":
                connection["ip"] = "127.0.0.1"
                connection["port"] = 8080

                state = "INGAME"

            if state == "CONNECTING_CUSTOM":
                fill_screen()
                blit_text("Please open the console!", 600, 400, 72)
                pygame.display.update()
                connection["ip"] = input("INPUT > Please input the server IP: ")
                connection["port"] = input("INPUT > Please input the server PORT: ")

                state = "INGAME"

        # Game handler
        if state.startswith("INGAME"):
            fill_screen()
            pygame.display.update()

            # TODO: Fix loop erroring
            loop.create_task(frame())
            loop.run_forever()
            print("done?")
            loop.close()

        # Help page
        if state.startswith("HELP"):
            None

        # Updates screen and FPS clock
        pygame.display.update()
        clock.tick(60)
        # print("FPS > " + str(clock.get_fps()))
        # print(state)

# Asyncronus game loop that connects with the websocket
async def frame():
    global start_time
    global frame_interval
    try:
        async with websockets.connect("ws://" + connection["ip"] + ":" + str(connection["port"])) as websocket:
            start_time = time.time()
            join_packet = {
                "name": "JOIN",
                "player_name": "testing"
            }
            await websocket.send(json.dumps(join_packet))
            print('WEBSOCKET > {}'.format(json.dumps(join_packet)) + ' TO ' + str(websocket))

            raw_ack = await websocket.recv()
            print('WEBSOCKET < {}'.format(raw_ack) + ' ON ' + str(websocket))
            player_id = json.loads(raw_ack)["player_id"]
            websocket_state = {}
            next_heartbeat = {}

            while True:
                await asyncio.sleep(frame_interval - ((time.time() - start_time) % frame_interval))

                next_heartbeat = {
                    'name': 'KEY',
                    'player_id': player_id,
                    'keys': [
                        {
                            'action': 'UP',
                            'change': 'KEY_UP'
                        },
                        {
                            'action': 'DOWN',
                            'change': 'KEY_UP'
                        },
                        {
                            'action': 'LEFT',
                            'change': 'KEY_UP'
                        },
                        {
                            'action': 'RIGHT',
                            'change': 'KEY_UP'
                        },
                        {
                            'action': 'HEAVY',
                            'change': 'KEY_UP'
                        }
                    ]
                }

                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.QUIT:
                        break
                    if keys[pygame.K_UP] != 0 or keys[pygame.K_w] != 0:
                        next_heartbeat['keys'][0]['change'] = 'KEY_DOWN'
                    if keys[pygame.K_DOWN] != 0 or keys[pygame.K_d] != 0:
                        next_heartbeat['keys'][1]['change'] = 'KEY_DOWN'
                    if keys[pygame.K_LEFT] != 0 or keys[pygame.K_a] != 0:
                        next_heartbeat['keys'][2]['change'] = 'KEY_DOWN'
                    if keys[pygame.K_RIGHT] != 0 or keys[pygame.K_d] != 0:
                        next_heartbeat['keys'][3]['change'] = 'KEY_DOWN'
                    if keys[pygame.K_SPACE] != 0 or keys[pygame.K_x] != 0 or keys[pygame.KMOD_SHIFT] != 0:
                        next_heartbeat['keys'][4]['change'] = 'KEY_DOWN'

                fill_screen()

                await websocket.send(json.dumps(next_heartbeat))
                print('WEBSOCKET > {}'.format(json.dumps(next_heartbeat)) + ' TO ' + str(websocket))

                websocket_state = json.loads(await websocket.recv())
                print('WEBSOCKET < {}'.format(websocket_state) + ' ON ' + str(websocket))

                players = websocket_state["players"]
                map_objects = websocket_state["map"]["objects"]
                for obj in map_objects:
                    if obj["type"] == "rect":
                        pygame.draw.rect(screen, (0, 0, 0), (obj["x"], obj["y"], obj["x_len"], obj["y_len"]))
                    if obj["type"] == "circle":
                        pygame.draw.circle(screen, (0, 0, 0), (obj["x"], obj["y"]), obj["radius"])

                for key in players:
                    player = players[key]
                    player_loc = player["location"]
                    player_name = player["name"]

                    if not player["spectator"]:
                        alpha_rect((int(player_loc[0]), int(player_loc[1] - 75)), (50, 25), (0, 0, 0), 50)
                        pygame.gfxdraw.filled_circle(screen, int(player_loc[0]), int(player_loc[1]), 25, (255, 255, 255))

                pygame.display.update()
    except:
        print("ERROR > Connection error has occured. Exiting to the menu...")
    finally:
        reset()
        return


# Runs the main loop, and exits the process when main terminates
main()
sys.exit()
