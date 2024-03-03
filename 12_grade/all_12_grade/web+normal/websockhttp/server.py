import asyncio
import json
import serial
import websockets

point = []
dofek = 0

async def handle_client(websocket, path):
    global dofek
    try:
        async for request in websocket:
            if request == "get_data":
                print("Sending data...")
                await websocket.send(json.dumps(dofek))
            else:
                print(f"Received invalid request: {request}")
    except websockets.exceptions.ConnectionClosed:
        pass

async def arduino():
    global dofek
    # Define the serial port and baud rate
    serial_port = 'COM5'  # Change this to the appropriate port
    baud_rate = 9600

    # Connect to the Arduino board
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    try:
        while True:
            # Wait for a message from Arduino
            response = ser.readline().decode('utf-8').strip()
            if response:
                # if int(response) == 100100:
                #     response = 10000
                dofek = int(response) // 55.5 + 40
    finally:
        ser.close()  # Close the serial port when done

async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_client, "localhost", 5000):
        print("WebSocket server is running on ws://localhost:5000")
        # Start the Arduino communication
        await arduino()

if __name__ == "__main__":
    asyncio.run(main())
