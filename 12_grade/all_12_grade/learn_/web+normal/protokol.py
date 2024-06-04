import os
import socket
import ssl
import base64
import hashlib
import struct
import threading
import subprocess


class Web_Socket:
    def __init__(self, host, port, certfile, keyfile):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def generate_self_signed_cert(self):
        if not os.path.exists(self.certfile) or not os.path.exists(self.keyfile):
            print("Generating self-signed certificate...")
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-keyout', self.keyfile,
                '-out', self.certfile, '-days', '365', '-nodes',
                '-subj', '/CN=localhost'
            ])
            print("Certificate and key have been generated.")

    def run_server(self):
        self.generate_self_signed_cert()

        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_socket.bind((self.host, self.port))
        raw_socket.listen(5)

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)

        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = raw_socket.accept()
            try:
                print(client_socket)
                ssl_client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
                print("New connection from:", client_address)
                client_thread = threading.Thread(target=self.handle_client, args=(ssl_client_socket,))
                client_thread.start()
            except ssl.SSLError as e:
                print(f"SSL error: {e}")
                client_socket.close()

    def handle_client(self, client_socket):
        try:
            self.accept_connection(client_socket)
            while True:
                data = self.receive_data(client_socket)
                if data is None:
                    print("Connection closed by client.")
                    break
                print("Received message:", data)
                self.send_data(client_socket, data)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def accept_connection(self, client_socket):
        try:
            data = client_socket.recv(1024)
            headers = data.decode('utf-8').split('\r\n')

            key = None
            for header in headers:
                if header.startswith('Sec-WebSocket-Key:'):
                    key = header.split(' ')[1]
                    break

            response_key = base64.b64encode(hashlib.sha1((key + self.GUID).encode()).digest()).decode()
            response = "HTTP/1.1 101 Switching Protocols\r\n"
            response += "Upgrade: websocket\r\n"
            response += "Connection: Upgrade\r\n"
            response += "Sec-WebSocket-Accept: " + response_key + "\r\n\r\n"
            client_socket.send(response.encode())
        except UnicodeDecodeError as e:
            print(f"Unicode decode error: {e}")
        except Exception as e:
            print(f"Error during WebSocket handshake: {e}")

    @staticmethod
    def send_data(client_socket, data):
        try:
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
        except Exception as e:
            print(f"Error sending data: {e}")

    @staticmethod
    def receive_data(client_socket):
        try:
            data = client_socket.recv(1024)
            if not data:
                return None

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
            return payload.decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"Unicode decode error: {e}")
            return None
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8765
    CERTFILE = 'server.crt'
    KEYFILE = 'server.key'

    websocket_server = Web_Socket(HOST, PORT, CERTFILE, KEYFILE)
    websocket_server.run_server()
