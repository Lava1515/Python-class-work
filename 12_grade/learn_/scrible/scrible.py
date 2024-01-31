import asyncio
import websockets

# Dictionary to store all connected clients
clients = set()

async def handle_client(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the received message to all connected clients
            await asyncio.gather(
                client.send(message)
                for client in clients
                if client != websocket
            )
    finally:
        # Remove the client from the set when they disconnect
        clients.remove(websocket)

if __name__ == "__main__":
    start_server = websockets.serve(handle_client, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
