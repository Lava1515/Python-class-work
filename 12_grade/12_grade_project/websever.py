import socket
import base64
import hashlib
import struct
import threading

# Define constants
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def accept_connection(client_socket):
    data = client_socket.recv(1024).decode().strip()
    headers = data.split('\r\n')

    # Extract key from headers
    key = None
    for header in headers:
        if header.startswith('Sec-WebSocket-Key:'):
            key = header.split(' ')[1]

    # Generate response
    response_key = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
    response = "HTTP/1.1 101 Switching Protocols\r\n"
    response += "Upgrade: websocket\r\n"
    response += "Connection: Upgrade\r\n"
    response += "Sec-WebSocket-Accept: " + response_key + "\r\n\r\n"

    client_socket.send(response.encode())


def send_data(client_socket, data):
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

    client_socket.send(header + payload)


def receive_data(client_socket):
    #todo make it work to more then 1024 and put in while
    data = client_socket.recv(1024)

    # Parse WebSocket frame
    if len(data) > 6:
        payload_length = data[1] & 127
        if payload_length == 126:
            mask = data[4:8]
            raw_payload = data[8:]
        elif payload_length == 127:
            mask = data[10:14]
            raw_payload = data[14:]
        else:
            mask = data[2:6]
            raw_payload = data[6:]

        payload = bytearray([raw_payload[i] ^ mask[i % 4] for i in range(len(raw_payload))])
        return payload.decode()


def handle_client(client_socket):
    accept_connection(client_socket)

    while True:
        data = receive_data(client_socket)
        if data:
            print("Received from client:", data)
            response = input("Enter data to send to client: ")
            send_data(client_socket, response)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8765))
    server_socket.listen(5)

    print("WebSocket server running on port 8765")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
