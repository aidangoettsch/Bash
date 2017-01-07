import websockets
import asyncio

async def hello():
    async with websockets.connect('ws://localhost:8080') as websocket:
        while True:
            name = input("What's your name? ")
            await websocket.send(name)
            print("> {}".format(name))

            greeting = await websocket.recv()
            print("< {}".format(greeting))
            websocket.close()

asyncio.ensure_future(hello())
asyncio.get_event_loop().run_forever()
