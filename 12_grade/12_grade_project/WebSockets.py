import base64
import hashlib
import struct


class Web_Socket:
    def __init__(self):
        self.GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    # Define constants

    def accept_connection(self, client_socket):
        data = client_socket.recv(1024).decode().strip()
        headers = data.split('\r\n')
        # Extract key from headers
        key = None
        for header in headers:
            if header.startswith('Sec-WebSocket-Key:'):
                key = header.split(' ')[1]
        # Generate response
        response_key = base64.b64encode(hashlib.sha1((key + self.GUID).encode()).digest()).decode()
        response = "HTTP/1.1 101 Switching Protocols\r\n"
        response += "Upgrade: websocket\r\n"
        response += "Connection: Upgrade\r\n"
        response += "Sec-WebSocket-Accept: " + response_key + "\r\n\r\n"
        client_socket.send(response.encode())

    @staticmethod
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

    @staticmethod
    def receive_data(client_socket):
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
