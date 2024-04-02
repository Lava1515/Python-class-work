import asyncio
import websockets
import base64
import hashlib
import struct

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

# Store connected clients
connected = set()

async def accept_connection(websocket, path):
    # Extract key from headers
    key = None
    async for header in websocket:
        if header.startswith('Sec-WebSocket-Key:'):
            key = header.split(' ')[1]

    # Generate response
    response_key = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
    response = "HTTP/1.1 101 Switching Protocols\r\n"
    response += "Upgrade: websocket\r\n"
    response += "Connection: Upgrade\r\n"
    response += "Sec-WebSocket-Accept: " + response_key + "\r\n\r\n"

    # Send response
    await websocket.send(response)

async def send_data(websocket, data):
    # Create WebSocket frame
    header = bytearray()
    header.append(0b10000001)  # FIN + Text opcode
    payload = bytearray(data.encode())
    payload_length = len(payload)

    if payload_length <= 125:
        header.append(payload_length)
    elif payload_length <= 65535:
        header.append(126)
        header.extend(struct.pack("!H", payload_length))
    else:
        header.append(127)
        header.extend(struct.pack("!Q", payload_length))

    # Send frame
    await websocket.send(header + payload)

async def handler(websocket, path):
    # Accept connection
    await accept_connection(websocket, path)
    # Register client
    connected.add(websocket)
    try:
        async for message in websocket:
            # Broadcast message to all connected clients
            for ws in connected:
                if ws != websocket:  # Avoid sending message back to sender
                    await send_data(ws, message)
    finally:
        # Remove client when connection is closed
        connected.remove(websocket)

# Start websocket server
start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
