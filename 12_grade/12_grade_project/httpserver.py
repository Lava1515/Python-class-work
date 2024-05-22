import json
import socket
import threading

import serial
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import constans
from protocol import Protocol
from WebSockets import Web_Socket


class WebServer:
    def __init__(self, DataBase):
        self.database = DataBase
        self.server_socket = None
        self.chats = {}
        self.clients = set()
        self.response = ""

    def handle_client(self, client_socket):
        res_data = ""
        self.clients.add(client_socket)
        try:
            request = client_socket.recv(1024).decode()
            data = request.split("\r\n\r\n")[-1]
            method, path, *_ = request.split()
            if "GET" in method:
                if path == '/':
                    path = "/Login.html"
                    self.send_files(client_socket, path, "ok")

                elif "/get_coaches" in path:
                    names = self.database.accounts_details.find({"Permissions": "Coach"})
                    namelist = [name["name"].lower() for name in names]
                    print(namelist)
                    res_data = json.dumps(namelist)

                elif path != "/" and "?" not in path:
                    self.send_files(client_socket, path, "ok")

                self.response = (constans.HTTP + constans.STATUS_CODES["ok"]
                                 + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]
                                 + constans.CONTENT_LENGTH + str(len(res_data))
                                 + "\r\n\r\n" + res_data)
            elif 'POST' in method:
                if "/send_details_Login" in path:
                    acc = json.loads(data)
                    result = self.database.accounts_details.find_one({"name": acc["name"].lower()})
                    print(result)
                    res_data = json.dumps({"can_login": "false"})
                    if result is not None and result["password"] == acc["pass"]:
                        res_data = json.dumps({"can_login": "true"})

                elif "/send_details_Register" in path:
                    acc = json.loads(data)
                    result = self.database.accounts_details.find_one({"name": acc["name"].lower()})
                    if result is None:
                        self.database.accounts_details.insert_one(
                            {"name": acc["name"].lower(), "password": acc["pass"], "Permissions": "Trainer"})
                        res_data = json.dumps({"existing": "false"})
                    else:
                        res_data = json.dumps({"existing": "true"})

                elif "/AdminRegister" in path:
                    acc = json.loads(data)
                    all_names = self.database.accounts_details.find_one({"name": acc["name"].lower()})
                    if all_names is None:
                        self.database.accounts_details.insert_one(
                            {"name": acc["name"].lower(), "password": acc["pass"], "Permissions": "Coach"})
                        res_data = json.dumps({"existing": "false"})
                    else:
                        res_data = json.dumps({"existing": "true"})

                elif "/add_contact" in path:
                    data = json.loads(data)
                    friend_name = data["data"].lower()
                    current_user_name = data["current_user"].lower()

                    # Check if the friend exists in the database
                    friend = self.database.accounts_details.find_one({"name": friend_name})
                    if friend:
                        # Check if the current user exists in the database
                        user = self.database.accounts_details.find_one({"name": current_user_name})
                        if user:
                            # Check if the friend already exists for the user
                            if friend_name in user.get("friends", []):
                                res_data = json.dumps({"existing": True})
                            else:
                                # Add the friend to the user's friends list
                                self.database.accounts_details.update_one({"name": current_user_name},
                                                                          {"$push": {"friends": friend_name}})
                                res_data = json.dumps({"existing": False})
                        else:
                            res_data = json.dumps({"error": "User not found"})
                    else:
                        res_data = json.dumps({"error": "Contact not found"})

                elif "/create_group" in path:
                    # :todo crate group
                    data = json.loads(data)
                    print(data)
                    res_data = json.dumps({"existing": "true"})

                elif "/SetCoach" in path:
                    data = json.loads(data)
                    coach_name = data["coach"].lower()
                    current_user_name = data["current_user"].lower()

                    # Check if coach exists
                    coach = self.database.accounts_details.find_one({"name": coach_name, "Permissions": "Coach"})
                    if coach:
                        # Check if current user exists
                        user = self.database.accounts_details.find_one({"name": current_user_name})
                        if user:
                            # Check if current user already has a coach
                            if not user.get("coach"):
                                # Update current user's coach and add current user to coach's trainers
                                self.database.accounts_details.update_one(
                                    {"name": current_user_name},
                                    {"$set": {"coach": coach_name}}
                                )
                                self.database.accounts_details.update_one(
                                    {"name": coach_name},
                                    {"$push": {"trainers": current_user_name}}
                                )
                                res_data = json.dumps({"Added": True})
                            else:
                                res_data = json.dumps({"error": "This user already has a coach"})
                        else:
                            res_data = json.dumps({"error": "User not found"})
                    else:
                        res_data = json.dumps({"error": "Coach not found"})

                elif "/get_Permissions" in path:
                    data = json.loads(data)
                    account = self.database.accounts_details.find_one({"name": data["current_user"].lower()})
                    print(data)
                    res_data = json.dumps({"Permissions": account["Permissions"]})

                elif "/get_trainers" in path:
                    data = json.loads(data)
                    account = self.database.accounts_details.find_one({"name": data["current_user"].lower()})
                    print(data)
                    res_data = json.dumps({"Trainers": account["trainers"]})
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
    def send_files(client_socket, path, status_code):
        type_ = path.split(".")[-1]
        path = "webroot/" + path
        try:
            with open(path, 'rb') as file:
                content = file.read()
                content_type = constans.CONTENT_TYPE + constans.FILE_TYPE[type_]
                content_length = constans.CONTENT_LENGTH + str(len(content)) + "\r\n"
                http_response = constans.HTTP + constans.STATUS_CODES[
                    status_code] + content_type + content_length + "\r\n"
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
        print("Register as an Admin http://127.0.0.1:5000/AdminRegister.html")
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
    def __init__(self, DataBase, WebSocketInstance):
        self.database = DataBase
        self.WS = WebSocketInstance
        self.protocol = Protocol()

    def start_arduino(self):
        # Server configuration
        HOST = '0.0.0.0'
        PORT = 5555
        try:
            self.protocol.bind((HOST, PORT))
            self.protocol.listen()
            print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
            while True:
                client_socket, addr = self.protocol.accept()
                print(f"[CONNECTED] Connection from {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()

        except KeyboardInterrupt:
            print("[STOPPING] Server is stopping")
        finally:
            self.protocol.close()

    def handle_client(self, client_socket):
        while True:
            try:
                method, data = client_socket.get_msg().decode().split(":")
                if "check_user" in method:
                    print("logi")
                    username, password = data.split(",")
                    result = self.database.accounts_details.find_one({"name": username.lower()})
                    if result is not None and result["password"] == password:
                        client_socket.send_msg("Success")
                        print("Success")
                    else:
                        client_socket.send_msg("Failure")
                        print("Failure")
                elif method == "bpm":
                    print(data)
            except Exception as e:
                print(f"Error handling client: {e}")
                break


class WebSocket(Web_Socket):
    def __init__(self):
        super().__init__()
        self.clients = {}

    def handle_client(self, client_socket, addr):
        self.accept_connection(client_socket)
        client_name = self.receive_data(client_socket)
        self.clients[client_name] = client_socket
        print(self.clients)
        while True:
            try:
                data = self.receive_data(client_socket)
                # if data.split(' ')[0] in self.clients.keys():
                #     self.send_data(self.clients[data.split(' ')[0]], data)
                print("Received from client:", data)
            except Exception:  # there's 3 different exceptions
                print(f"the client {addr} disconnected")
                break

    def start_websockets(self):
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8765))
        server_socket.listen(5)

        print("WebSocket server running on port 8765")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_handler.start()


class Server:
    def __init__(self):
        self.DataBase = self.open_database()
        self.web_server = WebServer(self.DataBase)
        self.web_socket = WebSocket()
        self.arduino = Arduino(self.DataBase, self.web_socket)
        self.users = {}

    @staticmethod
    def open_database():
        uri = "mongodb+srv://lavak:Lava@heartrate.qduwqzq.mongodb.net/?retryWrites=true&w=majority&appName=heartrate"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        print(client.list_database_names())
        return client.heartrate  # access database

    def start_server(self):
        web_thread = threading.Thread(target=self.web_server.start_server, daemon=True)
        websockets_tread = threading.Thread(target=self.web_socket.start_websockets, daemon=True)
        arduino_thread = threading.Thread(target=self.arduino.start_arduino, daemon=True)
        web_thread.start()
        websockets_tread.start()
        arduino_thread.start()
        web_thread.join()
        websockets_tread.join()
        arduino_thread.join()


def main():
    server = Server()
    server.start_server()


if __name__ == "__main__":
    main()
