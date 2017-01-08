import websockets
import asyncio

websocket = websockets.connect('ws://localhost:8080')

async def send():
    while True:
        name = input("SEND >  ")
        await websocket.send(name)
        print("WEBSOCKET > {}".format(name))

async def receive():
        while True:
            event = await websocket.recv()
            print("WEBSOCKET < {}".format(event))

loop = asyncio.get_event_loop()
loop.create_task(send())
loop.create_task(receive())
loop.run_forever()
