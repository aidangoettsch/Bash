import time
from src.common.state import State
from src.common.player import Player
import asyncio
import websockets
import json
import os


async def process_event(websocket, path):
    """
    Process an event sent to the server from a client

    :param websocket:
    :param path:
    :return:
    """
    event = await websocket.recv()
    event = json.loads(event)
    if event['name'] == 'JOIN':
        player = Player(websocket, event['player_name'])
        state.players.append(player)

start_server = websockets.serve(process_event, 'localhost', 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


def load_map(name):
    """
    Loads a map file into memory.

    :param name:
    :return:
    """
    file = open(os.path.join('..', 'maps', name + '.json'))
    state.map = json.loads(file.read())


def frame():
    """
    Process the physics for a frame and send the render command.

    :return:
    """
    global state

target_fps = 60.0
frame_interval = 1.0 / target_fps
start_time = time.time()

state = State()

while True:
    frame()
    time.sleep(frame_interval - ((time.time() - start_time) % frame_interval))
