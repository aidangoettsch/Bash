import time
from src.common.state import State
from src.common.player import Player
import asyncio
import websockets
import json
import os
import copy

target_fps = 1.0

frame_interval = 1.0 / target_fps

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
        print('WEBSOCKET < {}'.format(event) + ' FROM ' + str(websocket) + ' AT ' + str(path))

        confirm = {
            'name': 'ACK'
        }
        try:
            if event['name'] == 'JOIN':
                # Handle a player connecting.
                player = Player(websocket, event['player_name'])
                state.players[player.id] = player
                confirm['player_id'] = player.id
            elif event['name'] == 'KEY':
                # Handle a player pressing or releasing a key.
                if event['action'] == 'UP' and event['change'] == 'KEY_DOWN':
                    player = state.players[event['player_id']]
                    player.up = True
                elif event['action'] == 'UP' and event['change'] == 'KEY_UP':
                    player = state.players[event['player_id']]
                    player.up = False
                elif event['action'] == 'DOWN' and event['change'] == 'KEY_DOWN':
                    player = state.players[event['player_id']]
                    player.down = True
                elif event['action'] == 'DOWN' and event['change'] == 'KEY_UP':
                    player = state.players[event['player_id']]
                    player.down = False
                elif event['action'] == 'LEFT' and event['change'] == 'KEY_DOWN':
                    player = state.players[event['player_id']]
                    player.left = True
                elif event['action'] == 'LEFT' and event['change'] == 'KEY_UP':
                    player = state.players[event['player_id']]
                    player.left = False
                elif event['action'] == 'RIGHT' and event['change'] == 'KEY_DOWN':
                    player = state.players[event['player_id']]
                    player.right = True
                elif event['action'] == 'RIGHT' and event['change'] == 'KEY_UP':
                    player = state.players[event['player_id']]
                    player.right = False
                elif event['action'] == 'HEAVY' and event['change'] == 'KEY_DOWN':
                    player = state.players[event['player_id']]
                    player.right = True
                elif event['action'] == 'HEAVY' and event['change'] == 'KEY_UP':
                    player = state.players[event['player_id']]
                    player.right = False
            elif event['name'] == 'HEARTBEAT':
                confirm = send_state
            elif event['name'] == 'CLOSE':
                # Handle a player disconnecting.
                websocket.close()
                confirm['event'] = 'CLOSE'
            else:
                # Handle an unknown event
                confirm['name'] = 'UNKNOWN_EVENT'
        except KeyError:
            confirm['name'] = 'PARSE_EXCEPTION'

        await websocket.send(json.dumps(confirm))
        print('WEBSOCKET > {}'.format(confirm) + ' TO ' + str(websocket))


def load_map(name):
    """
    Loads a map file into memory.

    :param name:
    :return:
    """
    file = open(os.path.join('maps', name + '.json'))
    state.map = json.loads(file.read())
    for player in state.players:
        player.spectator = False


async def frame():
    """
    Process the physics for a frame and send the render command.

    :return:
    """
    global state
    global send_state
    state.start_time = time.time()
    # TODO: Add start round function
    load_map('test')
    while True:
        await asyncio.sleep(frame_interval - ((time.time() - state.start_time) % frame_interval))
        # print("frame")
        # print(json.dumps(state.__dict__))
        state.start_time = time.time()
        for player_id in state.players:
            player = state.players[player_id]
            if not player.spectator:
                # Check collisions
                for obj in state.map['objects']:
                    if obj.type == 'rect':
                        if (abs(player.location[0] - obj.x) < 50 + obj.x_len) and \
                                (abs(player.location[1] - obj.y) < obj.y_len):
                            player.velocity[1] *= -1
                        elif abs(player.location[1] - obj.y) < 50 + obj.y_len and \
                                (abs(player.location[0] - obj.x) < obj.x_len):
                            player.velocity[0] *= -1
                    elif obj.type == 'circle':
                        if abs(player.location[0] - obj.x) < 50 + obj.radius and \
                                (abs(player.location[1] - obj.y) < obj.radius):
                            player.velocity[1] *= -1
                        if abs(player.location[1] - obj.y) < 50 + obj.radius and \
                                (abs(player.location[0] - obj.x) < obj.radius):
                            player.velocity[0] *= -1
                for uuid in state.players:
                    if not uuid == player.id:
                        player2 = state.players[uuid]
                        if abs(player.location[0] - player.location[0]) < 50 + obj.radius and \
                                (abs(player.location[1] - player.location[1]) < obj.radius):
                            player.velocity[1] *= -1
                            player2.velocity[1] *= -1
                        if abs(player.location[1] - player.location[1]) < 50 + obj.radius and \
                                (abs(player.location[0] - player.location[0]) < obj.radius):
                            player.velocity[0] *= -1
                            player2.velocity[0] *= -1
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
                    player.velocity += v_change
                elif player.right and player.velocity[0] < v_max:
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

                # Player movement
                player.location[0] += player.velocity[0]
                player.location[1] += player.velocity[1]
        send_state = copy.copy(state).__dict__
        send_state['players'] = copy.copy(state.players)
        for player_id in state.players:
            send_state['players'][player_id] = copy.copy(state.players[player_id]).__dict__
            send_state['players'][player_id]['socket'] = None


print("INFO > Server starting")

# Create the event loop and queue the websocket server and game loop onto it
loop = asyncio.get_event_loop()
start_server = websockets.serve(process_event, 'localhost', 8080)
loop.create_task(start_server)
loop.create_task(frame())
loop.run_forever()

quit()
