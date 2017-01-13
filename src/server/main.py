import time
from src.common.state import State
from src.common.player import Player
import asyncio
import websockets
import json
import os
import copy
import random
import math

target_fps = 60.0
frame_interval = 1.0 / target_fps
gravity = 0.2
friction = 0.02
player_radius = 25

state = State()
send_state = {}

async def process_event(websocket, path):
    """
    Process an event sent to the server from a client

    :param websocket:
    :param path:
    :return:
    """
    while True:
        raw_event = await websocket.recv()
        event = json.loads(raw_event)
        # print('WEBSOCKET < {}'.format(event) + ' FROM ' + str(websocket) + ' AT ' + str(path))

        confirm = {
            'name': ''
        }
        try:
            if event['name'] == 'JOIN':
                # Handle a player connecting.
                player = Player(websocket, event['player_name'])
                state.players[player.id] = player
                confirm['player_id'] = player.id
                player.color = event['color']
                if len(state.players) == 1:
                    load_map('test')
            elif event['name'] == 'KEY':
                # Handle a player pressing or releasing a key.
                for key in event['keys']:
                    if key['action'] == 'UP' and key['change'] == 'KEY_DOWN':
                        player = state.players[event['player_id']]
                        player.up = True
                    elif key['action'] == 'UP' and key['change'] == 'KEY_UP':
                        player = state.players[event['player_id']]
                        player.up = False
                    elif key['action'] == 'DOWN' and key['change'] == 'KEY_DOWN':
                        player = state.players[event['player_id']]
                        player.down = True
                    elif key['action'] == 'DOWN' and key['change'] == 'KEY_UP':
                        player = state.players[event['player_id']]
                        player.down = False
                    elif key['action'] == 'LEFT' and key['change'] == 'KEY_DOWN':
                        player = state.players[event['player_id']]
                        player.left = True
                    elif key['action'] == 'LEFT' and key['change'] == 'KEY_UP':
                        player = state.players[event['player_id']]
                        player.left = False
                    elif key['action'] == 'RIGHT' and key['change'] == 'KEY_DOWN':
                        player = state.players[event['player_id']]
                        player.right = True
                    elif key['action'] == 'RIGHT' and key['change'] == 'KEY_UP':
                        player = state.players[event['player_id']]
                        player.right = False
                    elif key['action'] == 'HEAVY' and key['change'] == 'KEY_DOWN':
                        player = state.players[event['player_id']]
                        player.heavy = True
                    elif key['action'] == 'HEAVY' and key['change'] == 'KEY_UP':
                        player = state.players[event['player_id']]
                        player.heavy = False
                confirm = send_state
            elif event['name'] == 'HEARTBEAT':
                confirm = send_state
            elif event['name'] == 'CLOSE':
                # Handle a player disconnecting.
                websocket.close()
                confirm['event'] = 'CLOSE'
                confirm = send_state
            else:
                # Handle an unknown event
                confirm['name'] = 'UNKNOWN_EVENT'
        except KeyError:
            confirm['name'] = 'PARSE_EXCEPTION'

        await websocket.send(json.dumps(confirm))
        # print('WEBSOCKET > {}'.format(confirm) + ' TO ' + str(websocket))


def load_map(name):
    """
    Loads a map file into memory.

    :param name:
    :return:
    """
    file = open(os.path.join('maps', name + '.json'))
    state.map = json.loads(file.read())
    for player in state.players:
        player = state.players[player]
        player.spectator = False
        spawn = state.map['spawns'][random.randint(0, len(state.map['spawns']) - 1)]
        player.location = [spawn['x'], spawn['y']]
        player.velocity = [0, 0]


async def frame():
    """
    Process the physics for a frame and send the render command.

    :return:
    """
    global state
    global send_state
    global gravity
    global friction
    global frame_interval
    state.start_time = time.time()
    load_map('test')
    while True:
        await asyncio.sleep(frame_interval - ((time.time() - state.start_time) % frame_interval))
        state.start_time = time.time()
        for player_id in state.players:
            player = state.players[player_id]
            if not player.spectator:
                player.on_ground = False
                # Reflection
                for obj in state.map['objects']:
                    if obj['type'] == 'rect':
                        if abs(player.location[0] - obj['x']) <= player_radius + obj['x_len'] and \
                                (abs(player.location[1] - obj['y']) <= 0) and \
                                (abs(player.velocity[0]) > 1):
                            player.velocity[0] *= -1 * obj['bounce'] * (1.5 if player.heavy else 1)
                        if abs(player.location[1] - obj['y']) <= player_radius and \
                                (abs(player.location[0] - obj['x']) <= obj['x_len']):
                            if abs(player.velocity[1]) > 1:
                                player.velocity[1] *= -1 * obj['bounce'] * (1.5 if player.heavy else 1)
                            else:
                                player.velocity[1] = 0
                            player.on_ground = True
                    elif obj['type'] == 'circle':
                        if math.sqrt(abs(player.location[0] - obj['x']) ** 2 + abs(player.location[1] - obj['y']) ** 2) <= player_radius + obj['radius']:
                            player.velocity[0] *= -1 * (2 if player.heavy else 1.5)
                            player.velocity[1] *= -1 * (2 if player.heavy else 1.5)
                            player.on_ground = True
                for uuid in state.players:
                    if not uuid == player.id:
                        player2 = state.players[uuid]
                        if not player2.spectator:
                            if player.location == player2.location \
                                    and player.velocity == [0, 0] and player2.velocity == [0, 0]:
                                player.velocity = [0, 1]
                                player.location[0] += 100
                            elif math.sqrt(abs(player.location[0] - player2.location[0]) ** 2 + abs(player.location[1] - player2.location[1]) ** 2) <= player_radius * 2:
                                if player.velocity[0] < 1:
                                    player.velocity[0] = -1 * player2.velocity[0] * (1.5 if player.heavy else 0.75) * (1.5 if player2.heavy else 1)
                                if player2.velocity[0] < 1:
                                    player2.velocity[0] = -1 * player.velocity[0] * (1.5 if player.heavy else 0.75) * (1.5 if player2.heavy else 1)
                                if player.velocity[1] < 1 and not player.on_ground:
                                    player.velocity[1] = -1 * player2.velocity[1] * (1.5 if player.heavy else 1) * (1.5 if player2.heavy else 1)
                                if player2.velocity[1] < 1 and not player2.on_ground:
                                    player2.velocity[1] = -1 * player.velocity[1] * (1.5 if player.heavy else 1) * (1.5 if player2.heavy else 1)

                                player.velocity[0] *= -1
                                player.velocity[1] *= -1
                                player2.velocity[0] *= -1
                                player2.velocity[1] *= -1
                # Gravity and friction
                if not player.on_ground:
                    player.velocity[1] += gravity
                else:
                    player.velocity[0] *= 1 - friction
                # Handle player input and velocity changes.
                v_max = 20
                if player.velocity[0] < -1 * v_max:
                    player.velocity[0] = v_max
                if player.left and player.velocity[0] > -1 * v_max:
                    v_max_per_frame = -1
                    v_max_point = -10
                    if player.velocity[0] > 0:
                        v_change = v_max_per_frame
                    elif player.velocity[0] < v_max_point:
                        v_change = (player.velocity[0] / v_max_point) * v_max_per_frame
                    else:
                        v_change = v_max_per_frame / 5
                    if v_change < v_max_per_frame / 10:
                        v_change = v_max_per_frame / 10
                    player.velocity[0] += v_change
                if player.right and player.velocity[0] < v_max:
                    v_max_per_frame = 1
                    v_max_point = 10
                    if player.velocity[0] < 0:
                        v_change = v_max_per_frame
                    elif player.velocity[0] > v_max_point:
                        v_change = (player.velocity[0] / v_max_point) * v_max_per_frame
                    else:
                        v_change = v_max_per_frame / 5
                    if v_change < v_max_per_frame / 10:
                        v_change = v_max_per_frame / 10
                    player.velocity[0] += v_change
                if player.up and player.velocity[0] < v_max and player.on_ground:
                    player.velocity[1] -= 5
                    player.location[1] -= 0.1
                if player.down and player.velocity[0] < v_max and player.on_ground:
                    player.velocity[1] += 0.1
                # Handle death
                if player.location[0] < -200 or player.location[0] > 1400 \
                        or player.location[1] < -200 or player.location[1] > 900:
                    player.spectator = True
                # Move player
                player.location[0] += player.velocity[0]
                player.location[1] += player.velocity[1]
        players_alive = 0
        for player_id in state.players:
            if not state.players[player_id].spectator:
                players_alive += 1
        if players_alive == 1:
            load_map('test')
        # Prepare websocket state
        send_state = copy.copy(state).__dict__
        send_state['players'] = copy.copy(state.players)
        for player_id in state.players:
            send_state['players'][player_id] = copy.copy(state.players[player_id]).__dict__
            send_state['players'][player_id]['socket'] = None


print("INFO > Server starting")

# Create the event loop and queue the websocket server and game loop onto it
loop = asyncio.get_event_loop()
start_server = websockets.serve(process_event, '0.0.0.0', 8080)
loop.create_task(start_server)
loop.create_task(frame())
loop.run_forever()

quit()
