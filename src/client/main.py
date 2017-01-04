# import asyncio
# import websockets
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
# font_slabo_reg = pygame.freetype.Font('resources/Slabo_REG.ttf', 27) TODO: Fix fonts
screen = pygame.display.set_mode((200, 200))
state = "MENU"

# Core Functions
def render_menu():
    """
    Renders the menu screen

    :return:
    """
    # Background color
    screen.fill(pygame.Color(0, 150, 136))

    # Buttons
    pygame.draw.rect()

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    render_menu()
    pygame.display.update()




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
