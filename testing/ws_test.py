import websockets
import asyncio

# Connect
socket = websockets.connect('ws://localhost:8080')


async def listen():
    res = await socket.recv()
    print(res)

asyncio.get_event_loop().run_until_complete(listen)
asyncio.get_event_loop().run_forever()

while True:
    send = input("send: ")
    socket.send(send)
