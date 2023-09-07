import asyncio
import websockets

# Maintain a list of connected clients
connected_clients = set()


async def register(websocket):
    # Add a new client to the list
    connected_clients.add(websocket)


async def unregister(websocket):
    # Remove a client from the list
    connected_clients.remove(websocket)


async def broadcast(message):
    # Send a message to all connected clients
    if connected_clients:
        await asyncio.gather(
            *(client.send(message) for client in connected_clients))


async def echo(websocket, path):
    try:
        await register(websocket)
        async for message in websocket:
            # Broadcast the received message to all clients
            await broadcast(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
