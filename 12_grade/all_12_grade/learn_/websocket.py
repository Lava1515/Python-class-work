import asyncio
import websockets


async def handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send("Hello from Python server")
    except websockets.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server is running on ws://localhost:8080")
asyncio.get_event_loop().run_forever()
