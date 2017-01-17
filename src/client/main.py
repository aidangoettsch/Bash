# =====[ BASH // PYGAME PROJECT ]=====
# - File Purpose: Client
# - File Created: 1/8/2017
# - Contributors: CF12, yayes2

# Import Libraries
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
import re

# Initialize and check pygame initialization
try:
    pygame.init()
except:
    print("Pygame initialization failed. Check your game installation.")
    sys.exit()

# Sets the title of the window
pygame.display.set_caption("BASH - Created by Aidan G. & Brian X.")

# =====[ VARIABLE DECLARATIONS ]=====
# Screen related variables
screen_w = 1200
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))

# Time related variables
clock = pygame.time.Clock()
target_fps = 60.0
frame_interval = 1.0 / target_fps
start_time = time.time()

# Player related variables
username = "New Player"
player_color = (255, 0, 0)

# Connection related variables
default_connection = {
    "ip": "lccnetwork.dynu.net",
    "port": 8080
}
connection = {}

events = {
    "MOUSEDOWN": False,
    "KEY": None,
    "KEY_THROTTLE": False
}


# Other variables
mouse = pygame.mouse
def_font = pygame.freetype.Font('src/client/resources/Slabo_REG.ttf', 27)
regex = {
    "numbers": re.compile("[0-9]"),
    "period": re.compile("[.]")
}


# =======================================================
# States of the game
# This variable controls the client, and what it renders
# =======================================================
# MENU = Main menu screen
# CONNECTING_LOCALHOST = Connecting to localhost server
# CONNECTING_MAIN = Connecting to the main server
# INGAME_SETTINGS = In the nickname and color selection screen
# INGAME = In the game and playing
# =======================================================

state = "MENU"


# Core Functions
def render_menu():
    """
    Renders the main menu screen

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
        # MenuButton("Help", 350, 500, 500, 80, on_click_show_help)
    ]


def fill_screen():
    """
    Fills the background of the screen based on the state variable, and applies shadow if necessary

    """
    # Globals
    global menu, state

    # Detects states and fills background based on it
    if state.startswith("MENU"):
        screen.fill((0, 150, 136))
    if state.startswith("CONNECTING"):
        screen.fill((0, 96, 100))
        menu["shadow"].fade_in(120)
    if state.startswith("HELP"):
        screen.fill((0, 150, 136))
        menu["shadow"].fade_in(120)
    if state.startswith("INGAME"):
        screen.fill((0, 96, 100))


def blit_text(text, x, y, color, text_size, bold=False, center=True):
    """
    Blits text to the screen

    """
    # Globals
    global menu

    # Bolds the text if bold is True
    if bold:
        text_surface = def_font.render(text, fgcolor=color, style=pygame.freetype.STYLE_STRONG, size=text_size)
    else:
        text_surface = def_font.render(text, fgcolor=color, size=text_size)

    # Centers the text if center is True
    if center:
        screen.blit(text_surface[0], text_surface[0].get_rect(center=(x, y)))
    elif center is False:
        screen.blit(text_surface[0], (x, y))
    elif center == "LCenter":
        trect = text_surface[0].get_rect(center=(x, y))
        trect[0] = x
        screen.blit(text_surface[0], trect)

    # Returns the surface so it can be used further
    return text_surface


def alpha_rect(loc, size, color, opacity, center=False):
    """
    Creates a surface filled with a color that can have adjustable opacity

    """
    # Creates surface, fills it, and opacitizes it
    rect = pygame.Surface(size)
    rect.set_alpha(opacity)
    rect.fill(color)

    # Blits it to the screen based, and centers the surface if center is True
    if center:
        screen.blit(rect, rect.get_rect(center=loc))
    else:
        screen.blit(rect, loc)


def player_tag(name, loc):
    """
    Creates a player nametag at the location

    """
    # Creates an alpha_rect and blits it to the location
    tag_surface = blit_text(name, int(loc[0]), int(loc[1] - 50), (255, 255, 255), 12)
    tag_rect = tag_surface[0].get_rect(center=loc)
    alpha_rect((int(loc[0]), int(loc[1] - 50)), (tag_rect[2] + 20, tag_rect[3] + 15), (0, 0, 0), 50, center=True)


def reset():
    """
    Reset the game state after exiting from a game or when starting the game.
    Renders the portions of the client that are out of the game, such as the menu.

    """
    # Globals
    global state

    # Sets state to "MENU"
    state = "MENU"

    # Restarts the main loop
    main()


# Classes
class MenuButton():
    """
    Represents a menu button

    """

    def __init__(self, text, x, y, w, h, on_click_function):
        """
        Class constructor

        text = Text on the button
        x = X Location
        y = Y Location
        w = Button width
        h = Button height
        on_click_function = Function passed through to carry out what happens when the button is clicked

        """
        self.text                   = text
        self.x                      = x
        self.y                      = y
        self.w                      = w
        self.h                      = h
        self.mid_loc                = (x + w / 2, y + h / 2)
        self.on_click_function      = on_click_function

    def display_button(self):
        """
        Updates / draws the button

        """
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def display_text(self):
        """
        Updates / draws the text

        """
        self.button_text   = blit_text(self.text, self.mid_loc[0], self.mid_loc[1], (0, 0, 0), 32, bold=True)

    def on_hover(self):
        """
        Updates the button with the hover effects

        """
        self.button_fill   = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def off_hover(self):
        """
        Updates the button without the hover effects

        """
        self.button_fill   = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.button_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def on_click(self):
        """
        Calls the on_click_function() passed with the class construction

        """
        self.on_click_function()


class ColorButton():
    """
    Represents a color button

    """

    def __init__(self, x, y, w, h, color):
        """
        Class constructor

        x = X Location
        y = Y Location
        w = Width
        h = Height
        color = Color that the button represents

        """
        self.x                      = x
        self.y                      = y
        self.w                      = w
        self.h                      = h
        self.color                  = color
        self.selected               = False

    def display_button(self):
        self.button_fill   = pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        self.button_border = None

    def on_hover(self):
        self.button_border = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 3)

    def off_hover(self):
        self.button_border = None

    def check_selected(self):
        if self.selected:
            self.button_border = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 5)


class Shadow():
    """
    Represents a shadow backdrop behind everything

    """
    def __init__(self):
        self.opacity = 0
        self.shadow  = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)

    def fade_in(self, target):
        if self.opacity <= target:
            self.opacity += 6
        self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)

    def fade_out(self):
        if self.opacity >= 0:
            self.opacity -= 6
        self.shadow   = alpha_rect((0, 0), (1200, 800,), (0, 0, 0), self.opacity)


class TextBox():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text_box = None
        self.text = ""
        self.focused = False

    def display(self):
        self.box_fill = pygame.draw.rect(screen, (67, 190, 187), (self.x, self.y, self.w, self.h))
        self.box_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def on_hover(self):
        self.box_fill = pygame.draw.rect(screen, (167, 255, 235), (self.x, self.y, self.w, self.h))
        self.box_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def update_text(self):
        self.text_box = blit_text(self.text, self.x + 10, self.y + 18, (0, 0, 0), 24, center=False)

    def focus(self):
        if self.focused:
            self.box_fill = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h))
            self.box_border = pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h), 3)

    def type(self, char):
        self.text = str(self.text) + str(char)

    def backspace(self):
        self.text = self.text[:-1]

menu = {
    "buttons": [],
    "shadow": Shadow(),
    "ip_textbox": TextBox(300, 400, 600, 50),
    "username_textbox": TextBox(300, 400, 600, 50)
}

color_palette = {
    "red": ColorButton(400, 500, 100, 100, (255, 0, 0)),
    "blue": ColorButton(500, 500, 100, 100, (0, 0, 255)),
    "yellow": ColorButton(600, 500, 100, 100, (255, 255, 0)),
    "green": ColorButton(700, 500, 100, 100, (0, 255, 0))
}


def main():
    """
    This is the main game loop. Everything deviates from this function: Menus, the game itself, etc.

    * Returns nothing
    """
    global state, shadow_overlay, events, loop, username, player_color

    while True:
        # Pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                events["MOUSEDOWN"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                events["MOUSEDOWN"] = False
            if event.type == pygame.KEYDOWN:
                if event.unicode != '':
                    events["KEY"] = str(event.unicode)
            if event.type == pygame.KEYUP:
                events["KEY"] = None
                events["KEY_THROTTLE"] = False

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
                    blit_text("$bash_", 600, 100, (0, 0, 0), 84, bold=True)

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
            # Connection handlers
            if state == "CONNECTING_MAIN":
                connection["ip"] = "lccnetwork.dynu.net"
                connection["port"] = 8080

                state = "INGAME_SETTINGS"

            if state == "CONNECTING_LOCALHOST":
                connection["ip"] = "127.0.0.1"
                connection["port"] = 8080

                state = "INGAME_SETTINGS"

            if state == "CONNECTING_CUSTOM":
                menu["ip_textbox"].display()
                blit_text("Enter the IP to the server below:", 600, 325, (255, 255, 255), 52, bold=True)
                blit_text("Press ENTER to submit", 600, 700, (255, 255, 255), 32, bold=True)

                if events["MOUSEDOWN"]:
                    menu["ip_textbox"].focused = False

                if menu["ip_textbox"].box_fill.collidepoint(mouse.get_pos()):
                    menu["ip_textbox"].on_hover()

                    if events["MOUSEDOWN"]:
                        menu["ip_textbox"].focused = True
                else:
                    menu["ip_textbox"].display()
                menu["ip_textbox"].focus()

                if menu["ip_textbox"].focused:
                    if events["KEY"]:
                        if events["KEY"] == "\x08" and events["KEY_THROTTLE"] is False:
                            menu["ip_textbox"].backspace()
                        elif events["KEY_THROTTLE"] is False:
                            menu["ip_textbox"].type(events["KEY"])
                        events["KEY_THROTTLE"] = True

                if events["KEY"] == "\r":
                    connection["ip"] = menu["ip_textbox"].text
                    connection["port"] = 8080
                    state = "INGAME_SETTINGS"
                    events["KEY"] = None

                menu["ip_textbox"].update_text()

        if state == "INGAME_SETTINGS":
            menu["username_textbox"].display()
            blit_text("Enter a username & pick a color from below:", 600, 325, (255, 255, 255), 52, bold=True)
            blit_text("Press ENTER to submit", 600, 700, (255, 255, 255), 32, bold=True)

            for key in color_palette:
                button = color_palette[key]
                button.display_button()
                if button.button_fill.collidepoint(mouse.get_pos()):
                    button.on_hover()
                    if events["MOUSEDOWN"]:
                        player_color = button.color
                else:
                    button.off_hover()

            if events["MOUSEDOWN"]:
                menu["username_textbox"].focused = False

            if menu["username_textbox"].box_fill.collidepoint(mouse.get_pos()):
                menu["username_textbox"].on_hover()

                if events["MOUSEDOWN"]:
                    menu["username_textbox"].focused = True
            else:
                menu["username_textbox"].display()
            menu["username_textbox"].focus()

            if menu["username_textbox"].focused:
                if events["KEY"]:
                    if events["KEY"] == "\x08" and events["KEY_THROTTLE"] is False:
                        menu["username_textbox"].backspace()
                    elif events["KEY_THROTTLE"] is False:
                        menu["username_textbox"].type(events["KEY"])
                    events["KEY_THROTTLE"] = True

            if events["KEY"] == "\r":
                username = menu["username_textbox"].text
                state = "INGAME"

            menu["username_textbox"].update_text()

        # Game handler
        if state == "INGAME":
            fill_screen()
            pygame.display.update()

            loop.run_forever()

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
    global player_color
    # try:
    async with websockets.connect("ws://" + connection["ip"] + ":" + str(connection["port"])) as websocket:
        start_time = time.time()
        join_packet = {
            "name": "JOIN",
            "player_name": username,
            "color": [player_color[0], player_color[1], player_color[2]]
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

            keys = pygame.key.get_pressed()
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            fill_screen()

            await websocket.send(json.dumps(next_heartbeat))
            print('WEBSOCKET > {}'.format(json.dumps(next_heartbeat)) + ' TO ' + str(websocket))

            websocket_state = json.loads(await websocket.recv())
            print('WEBSOCKET < {}'.format(websocket_state) + ' ON ' + str(websocket))

            players = websocket_state["players"]
            map_objects = websocket_state["map"]["objects"]
            for obj in map_objects:
                if obj["type"] == "rect":
                    pygame.draw.rect(screen, (obj["fill"][0], obj["fill"][1], obj["fill"][2]), (obj["x"], obj["y"], obj["x_len"], obj["y_len"]))
                if obj["type"] == "circle":
                    pygame.gfxdraw.filled_circle(screen, obj["x"], obj["y"], obj["radius"], (obj["fill"][0], obj["fill"][1], obj["fill"][2]))

            for key in players:
                player = players[key]
                player_loc = player["location"]
                player_color = player["color"]
                player_name = player["name"]
                player_heavy = player["heavy"]

                if not player["spectator"]:
                    pygame.gfxdraw.filled_circle(screen, int(player_loc[0]), int(player_loc[1]), 25, (player_color[0], player_color[1], player_color[2]))
                    pygame.gfxdraw.aacircle(screen, int(player_loc[0]), int(player_loc[1]), 25, (player_color[0], player_color[1], player_color[2]))

                    player_tag(player_name, player_loc)
                    if player_heavy:
                        pygame.gfxdraw.filled_circle(screen, int(player_loc[0]), int(player_loc[1]), 25, (255, 255, 255))
                        pygame.gfxdraw.aacircle(screen, int(player_loc[0]), int(player_loc[1]), 25, (255, 255, 255))
                        pygame.gfxdraw.filled_circle(screen, int(player_loc[0]), int(player_loc[1]), 23, (player_color[0], player_color[1], player_color[2]))
                        pygame.gfxdraw.aacircle(screen, int(player_loc[0]), int(player_loc[1]), 23, (player_color[0], player_color[1], player_color[2]))

            pygame.display.update()
    reset()
    return

# Defines async loop
loop = asyncio.get_event_loop()
loop.create_task(frame())

# Runs the main loop, and exits the process when main terminates
main()
sys.exit()
