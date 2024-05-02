from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from protocol import Protocol
import threading
import constans
import hashlib
import serial
import socket
import base64
import struct
import time
import json


class WebServer:
    def __init__(self, DataBase):
        self.database = DataBase
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
                    acc = json.loads(data)
                    result = self.database.accounts_details.find_one({"name": acc["name"].lower()})
                    print(result)
                    res_data = json.dumps({"can_login": "false"})
                    if result is not None and result["password"] == acc["pass"]:
                        res_data = json.dumps({"can_login": "true"})
                    self.response = (constans.HTTP + constans.STATUS_CODES["ok"]
                                     + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]
                                     + constans.CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

                elif "/send_details_Register" in path:
                    acc = json.loads(data)
                    result = self.database.accounts_details.find_one({"name": acc["name"].lower()})
                    if result is None:
                        self.database.accounts_details.insert_one(
                            {"name": acc["name"].lower(), "password": acc["pass"]})
                        res_data = json.dumps({"existing": "false"})
                    else:
                        res_data = json.dumps({"existing": "true"})
                    self.response = (constans.HTTP + constans.STATUS_CODES["ok"]
                                     + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]
                                     + constans.CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)


                elif "/add_contact" in path:

                    data = json.loads(data)

                    print(data)

                    # Check if the user to be added exists in the database

                    friend_filter_query = {"name": data["data"]}

                    friend = self.database.accounts_details.find_one(friend_filter_query)

                    if friend:

                        # Friend found, proceed to add it

                        user_filter_query = {"name": data["current_user"]}

                        user = self.database.accounts_details.find_one(user_filter_query)

                        if user:

                            # Check if the friend already exists for the user

                            if data["data"] in user.get("fields", []):

                                # Friend already exists

                                res_data = json.dumps({"existing": True})

                            else:

                                # Friend does not exist, add it

                                update_query = {

                                    "$push": {"fields": data["data"]}

                                }

                                self.database.accounts_details.update_one(user_filter_query, update_query)

                                res_data = json.dumps({"existing": False})

                        else:

                            # User not found

                            res_data = json.dumps({"error": "User not found"})

                    else:

                        # Friend not found

                        res_data = json.dumps({"error": "Friend not found"})

                    self.response = (constans.HTTP + constans.STATUS_CODES["ok"]

                                     + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]

                                     + constans.CONTENT_LENGTH + str(len(res_data))

                                     + "\r\n\r\n" + res_data)

                    else:
                        # User not found
                        res_data = json.dumps({"error": "User not found"})
                    print(res_data)
                    self.response = (constans.HTTP + constans.STATUS_CODES["ok"]
                                     + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]
                                     + constans.CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

                elif "/create_group" in path:
                    data = json.loads(data)
                    print(data)
                    res_data = json.dumps({"existing": "true"})
                    self.response = (constans.HTTP + constans.STATUS_CODES["ok"]
                                     + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]
                                     + constans.CONTENT_LENGTH + str(len(res_data))
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
                content_type = constans.CONTENT_TYPE + constans.FILE_TYPE[type_]
                content_length = constans.CONTENT_LENGTH + str(len(content)) + "\r\n"
                http_response = constans.HTTP + constans.STATUS_CODES[status_code] + content_type + content_length + "\r\n"
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


class Arduino:
    def __init__(self, DataBase):
        self.database = DataBase
        self.heart_rate: int = 0
        self.WS = WebSocket(self.database)

    def handle_client_arduino(self, client_protocol, address):
        print(f"[NEW CONNECTION] {address} connected.")

        # Connect to WebSocket server
        ws_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ws_socket.connect(('localhost', 8765))

        # Accept WebSocket connection
        self.WS.accept_connection(ws_socket)

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
                self.WS.send_data(ws_socket, data.decode('utf-8'))
                # Echo the received data back to the client
                client_protocol.send_msg(data)
            except ConnectionError:
                print(f"[{address}] connection closed unexpectedly.")
                break
        # Close the WebSocket connection
        ws_socket.close()
        # Close the connection
        client_protocol.close()

    @staticmethod
    def get_bpm():
        ser = serial.Serial("COM3", 115200, timeout=1)
        serW = serial.Serial("COM4", 115200, timeout=1)
        avg_bmps = []
        last_ten = []
        count = 0
        avg = 0
        ok = True
        now = time.perf_counter()
        then = now
        try:
            while True:
                response = ser.readline().decode("utf-8").strip()
                if response:
                    data = int(response.split(",")[-1])
                    serW.write(response.encode() + b'\n')
                    if len(last_ten) >= 50:
                        last_ten.pop(0)
                    last_ten.append(data)
                    avg = int(sum(last_ten) / len(last_ten))
                    if ok and data >= avg + 3:
                        then = now
                        now = time.perf_counter()
                        if int(60 / (now - then)) > 220:
                            continue
                        count += 1
                        print("heartbeat", count)
                        if len(avg_bmps) >= 60:
                            avg_bmps.pop(0)
                        avg_bmps.append(60 / (now - then))
                        print(60 / (now - then))
                        print("avg", sum(avg_bmps) / len(avg_bmps))
                        ok = False
                    elif not ok:
                        now = time.perf_counter()
                        if int(60 / (now - then)) < 220 and data <= avg + 3:
                            ok = True
        finally:
            ser.close()
            
    def start_arduino(self):
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
            client_thread = threading.Thread(target=self.handle_client_arduino, args=(client_protocol, address), daemon=True)
            client_thread.start()


class WebSocket:
    def __init__(self, DataBase):
        self.database = DataBase
        self.GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        self.clients = {}
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

    def handle_client(self, client_socket):
        self.accept_connection(client_socket)
        client_name = self.receive_data(client_socket)
        self.clients[client_name] = client_socket
        print(self.clients)
        while True:
            data = self.receive_data(client_socket)
            if data.split(' ')[0] in self.clients.keys():
                self.send_data(self.clients[data.split(' ')[0]], data)
            print("Received from client:", data)
            # todo: recv data from database and send it

    def start_websockets(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8765))
        server_socket.listen(5)

        print("WebSocket server running on port 8765")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()


class Server:
    def __init__(self):
        self.DataBase = self.open_database()
        self.web_server = WebServer(self.DataBase)
        self.web_socket = WebSocket(self.DataBase)
        self.arduino = Arduino(self.DataBase)

    @staticmethod
    def open_database():
        uri = "mongodb+srv://lavak:Lava@heartrate.qduwqzq.mongodb.net/?retryWrites=true&w=majority&appName=heartrate"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        print(client.list_database_names())
        return client.heartrate  # access database

    def start_server(self):
        web_thread = threading.Thread(target=self.web_server.start_server, daemon=True)
        arduino_thread = threading.Thread(target=self.arduino.start_arduino, daemon=True)
        websockets_tread = threading.Thread(target=self.web_socket.start_websockets, daemon=True)
        web_thread.start()
        arduino_thread.start()
        websockets_tread.start()
        web_thread.join()
        arduino_thread.join()
        websockets_tread.join()


def main():
    server = Server()
    server.start_server()


if __name__ == "__main__":
    main()
