import asyncio
import websockets
import json

# Dummy data
data = {'name': 'John', 'age': 30, 'city': 'New York'}

async def send_data(websocket, path):
    # Send the data as JSON when a connection is established
    await websocket.send(json.dumps(data))

start_server = websockets.serve(send_data, "localhost", 8765)

print("Server started. Waiting for client connections...")

# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
