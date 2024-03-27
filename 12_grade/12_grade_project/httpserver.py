from datetime import datetime
from protocol import Protocol
import threading
import hashlib
import random
import serial
import socket
import base64
import struct
import time
import json

"""Http globals"""

WEB_ROOT = "webroot"
HTTP = "HTTP/1.1\r\n"
STRINGS = {"up": "/uploads/", "400": "/images/400.png", "404": "/images/404.png", "403": "/images/403.png",
           "500": "/images/403.png"}
CONTENT_TYPE = "Content-Type: "
CONTENT_LENGTH = "Content-Length: "
STATUS_CODES = {"ok": "200 OK\r\n", "bad": "400 BAD REQUEST\r\n", "not found": "404 NOT FOUND\r\n",
                "forbidden": "403 FORBIDDEN\r\n", "moved": "302 FOUND\r\n",
                "server error": "500 INTERNAL SERVER ERROR\r\n"}
FILE_TYPE = {"html": "text/html;charset=utf-8\r\n", "jpg": "image/jpeg\r\n", "css": "text/css\r\n",
             "js": "text/javascript; charset=UTF-8\r\n", "txt": "text/plain\r\n", "ico": "image/x-icon\r\n"
             , "gif": "image/jpeg\r\n", "png": "image/png\r\n", "svg": "image/svg+xml",
             "json": "application/json\r\n"}

point = []
dofek = 0


class WebServer:
    def __init__(self):
        self.server_socket = None
        self.chats = {}
        self.clients = set()
        self.response = ""

    @staticmethod
    def read_file(file_name):
        """ Read A File """
        with open(file_name, "rb") as f:
            data = f.read()
        return data

    def load_chat_messages(self, chat_id):
        filename = f'chats_data/{chat_id}_messages.json'
        try:
            with open(filename, 'r') as file:
                self.chats[chat_id] = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with numbering
            self.chats[chat_id] = []
            with open(filename, 'w') as file:
                json.dump(self.chats[chat_id], file)

    def handle_client(self, client_socket):
        self.clients.add(client_socket)
        try:
            request = client_socket.recv(1024).decode()
            data = request.split("\r\n\r\n")[-1]
            method, path, *_ = request.split()
            if "GET" in method:
                if path == '/':
                    path = "/Login.html"
                    self.send_response(client_socket, path, "ok")

                elif path != "/" and "?" not in path:
                    self.send_response(client_socket, path, "ok")

            elif 'POST' in method:
                if "/send_details_Login" in path:
                    try:
                        with open("accounts_details.json", 'r') as file:
                            details_ = json.load(file)
                    except Exception as e:
                        print(e)
                        with open("accounts_details.json", 'w') as file_:
                            details_ = {}
                            json.dump({}, file_)
                    acc = json.loads(data)
                    res_data = json.dumps({"can_login": "false"})
                    if acc["name"].lower() in details_.keys():
                        if acc["pass"] == details_[acc["name"].lower()]["pass"]:
                            res_data = json.dumps({"can_login": "true"})
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

                elif "/send_details_Register" in path:
                    try:
                        with open("accounts_details.json", 'r') as file:
                            details_ = json.load(file)
                    except Exception as e:
                        print(e)
                        with open("accounts_details.json", 'w') as file_:
                            details_ = {}
                            json.dump({}, file_)
                    acc = json.loads(data)
                    if acc["name"].lower() not in details_.keys():
                        details_[acc["name"].lower()] = {"pass": acc["pass"]}
                        with open("accounts_details.json", 'w') as file_:
                            json.dump(details_, file_)
                        res_data = json.dumps({"existing": "false"})
                    else:
                        res_data = json.dumps({"existing": "true"})
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

            else:
                self.response = "HTTP/1.1 404 Not Found\r\n\r\n"
        finally:
            client_socket.send(self.response.encode())
            client_socket.close()
            self.clients.remove(client_socket)

    def update_messages_file(self, chat_id):
        filename = f'chats_data/{chat_id}_messages.json'
        with open(filename, 'w') as file:
            json.dump(self.chats[chat_id], file)

    @staticmethod
    def send_response(client_socket, path, status_code):
        type_ = path.split(".")[-1]
        path = "webroot/" + path
        try:
            with open(path, 'rb') as file:
                content = file.read()
                content_type = CONTENT_TYPE + FILE_TYPE[type_]
                content_length = CONTENT_LENGTH + str(len(content)) + "\r\n"
                http_response = HTTP + STATUS_CODES[status_code] + content_type + content_length + "\r\n"
                http_response = http_response.encode() + content
                client_socket.send(http_response)

        except FileNotFoundError as e:
            print(e)
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            client_socket.send(response.encode())

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 5000))
        self.server_socket.listen(5)
        print("Server is running on http://127.0.0.1:5000")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            self.server_socket.close()








# Function to handle client connections
# def handle_client_arduino(client_protocol, address):
#     print(f"[NEW CONNECTION] {address} connected.")
#
#     # Echo loop
#     while True:
#         try:
#             # Receive data from the client
#             data = client_protocol.get_msg()
#             if not data:
#                 print(f"[{address}] disconnected.")
#                 break
#
#             print(f"[{address}] {data.decode('utf-8')}")
#             # todo: update database
#
#             # Echo the received data back to the client
#             client_protocol.send_msg(data)
#         except ConnectionError:
#             print(f"[{address}] connection closed unexpectedly.")
#             break
#
#     # Close the connection
#     client_protocol.close()


def handle_client_arduino(client_protocol, address):
    print(f"[NEW CONNECTION] {address} connected.")

    # Connect to WebSocket server
    ws_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ws_socket.connect(('localhost', 8765))

    # Accept WebSocket connection
    accept_connection(ws_socket)

    # Echo loop
    while True:
        try:
            # Receive data from the client
            data = client_protocol.get_msg()
            if not data:
                print(f"[{address}] disconnected.")
                break

            print(f"[{address}] {data.decode('utf-8')}")

            # Send data through WebSocket
            send_data(ws_socket, data.decode('utf-8'))

            # Echo the received data back to the client
            client_protocol.send_msg(data)
        except ConnectionError:
            print(f"[{address}] connection closed unexpectedly.")
            break

    # Close the WebSocket connection
    ws_socket.close()

    # Close the connection
    client_protocol.close()


def get_bpm():
    ser = serial.Serial("COM3", 115200, timeout=1)
    serW = serial.Serial("COM4", 115200, timeout=1)
    count = 0
    ok = True
    now = time.perf_counter()
    try:
        while True:
            response = ser.readline().decode("utf-8").strip()
            if response:
                data = response.split(",")[-1]
                serW.write(data.encode() + "\n".encode())
                time.sleep(0.02)
                if ok and int(data) == 347:
                    then = now
                    now = time.perf_counter()
                    count += 1
                    print("heartbeat", count)
                    print(60 /(now - then))
                    ok = False
                elif not ok and int(data) < 347:
                    ok = True
    finally:
        ser.close()

def arduino():
    # Server configuration
    HOST = '127.0.0.1'
    PORT = 5555

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create a Protocol instance
    server_protocol = Protocol(server_socket)

    # Bind the socket to the host and port
    server_protocol.bind((HOST, PORT))

    # Listen for incoming connections
    server_protocol.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    # Main loop to accept incoming connections
    while True:
        # Accept a new connection
        client_protocol, address = server_protocol.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client_arduino, args=(client_protocol, address), daemon= True)
        client_thread.start()








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
        response = input("Enter data to send to client: ")
        send_data(client_socket, response)
        data = receive_data(client_socket)
        print("Received from client:", data)
        # todo: recv data from database and send it


def start_websockets():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8765))
    server_socket.listen(5)

    print("WebSocket server running on port 8765")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()









def main():
    webserver = WebServer()
    web_thread = threading.Thread(target=webserver.start_server, daemon=True)
    arduino_thread = threading.Thread(target=arduino, daemon=True)
    websockets_tread = threading.Thread(target=start_websockets, daemon=True)
    web_thread.start()
    arduino_thread.start()
    websockets_tread.start()
    web_thread.join()
    arduino_thread.join()
    websockets_tread.join()


if __name__ == "__main__":
    main()

