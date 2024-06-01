import json
import random
import socket
import threading
from datetime import date, datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import constans
from WebSockets import Web_Socket  # ik know there is built in module
from protocol import Protocol


class WebServer:
    def __init__(self, DataBase, _WebSocket):
        self.database = DataBase
        self.web_socket = _WebSocket
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
                    res_data = json.dumps(namelist)

                elif path != "/" and "?" not in path:
                    self.send_files(client_socket, path, "ok")

                self.response = (constans.HTTP + constans.STATUS_CODES["ok"]
                                 + constans.CONTENT_TYPE + constans.FILE_TYPE["json"]
                                 + constans.CONTENT_LENGTH + str(len(res_data))
                                 + "\r\n\r\n" + res_data)
            elif 'POST' in method:
                data = json.loads(data)
                if "/send_details_Login" in path:
                    result = self.database.accounts_details.find_one({"name": data["name"].lower()})
                    print(result)
                    res_data = json.dumps({"can_login": "false"})
                    if result is not None and result["password"] == data["pass"]:
                        res_data = json.dumps({"can_login": "true"})

                elif "/send_details_Register" in path:
                    result = self.database.accounts_details.find_one({"name": data["name"].lower()})
                    if result is None:
                        self.database.accounts_details.insert_one(
                            {"name": data["name"].lower(), "password": data["pass"], "Permissions": "Trainer"})
                        res_data = json.dumps({"existing": "false"})
                    else:
                        res_data = json.dumps({"existing": "true"})

                elif "/AdminRegister" in path:
                    all_names = self.database.accounts_details.find_one({"name": data["name"].lower()})
                    if all_names is None:
                        self.database.accounts_details.insert_one(
                            {"name": data["name"].lower(), "password": data["pass"], "Permissions": "Coach"})
                        res_data = json.dumps({"existing": "false"})
                    else:
                        res_data = json.dumps({"existing": "true"})

                elif "/add_contact" in path:
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
                                self.database.accounts_details.update_one({"name": current_user_name.lower()},
                                                                          {"$push": {"friends": friend_name}})
                                res_data = json.dumps({"existing": False})
                        else:
                            res_data = json.dumps({"error": "User not found"})
                    else:
                        res_data = json.dumps({"error": "Contact not found"})

                elif "/create_group" in path:
                    chats = self.database.chats.find_one({"name": "CHATS_NAMES_IDS"})
                    if chats is None:
                        self.database.chats.insert_one({"name": "CHATS_NAMES_IDS"})
                        chats = self.database.chats.find_one({"name": "CHATS_NAMES_IDS"})

                    id_ = self.get_chat_id(chats)
                    self.database.chats.insert_one({"id": str(id_), "accounts":[data["current_user"].lower()]})
                    self.database.chats.update_one({"name": "CHATS_NAMES_IDS"},
                                                   {"$set": {id_: data["chat_name"]}})
                    self.database.accounts_details.update_one({"name": data["current_user"].lower()},
                                                              {"$push": {"chats_ids": id_}})
                    res_data = json.dumps({"added_chat": "true", "id": id_})

                elif "/SetCoach" in path:
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
                                    {"name": current_user_name.lower()},
                                    {"$set": {"coach": coach_name}}
                                )
                                self.database.accounts_details.update_one(
                                    {"name": coach_name.lower()},
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
                    account = self.database.accounts_details.find_one({"name": data["current_user"].lower()})
                    res_data = json.dumps({"Permissions": account["Permissions"]})

                elif "/get_trainers" in path:
                    account = self.database.accounts_details.find_one({"name": data["current_user"].lower()})
                    res_data = json.dumps({"Trainers": account["trainers"]})

                elif "/get_bpms_dates" in path:
                    account = self.database.bpms.find_one({"name": data["current_user"].lower()})
                    try:
                        dates = list(filter(lambda key: str(key) != "_id" and key != "name", account.keys()))
                        res_data = json.dumps({"dates": dates})
                    except AttributeError:
                        res_data = json.dumps({"dates": []})
                        print("no dates saved")

                elif "/get_date_bpms" in path:
                    print(data)
                    account = self.database.bpms.find_one({"name": data["current_user"].lower()})
                    try:
                        res_data = json.dumps({"bpms": account[data["date"]]})
                    except KeyError:
                        res_data = json.dumps({"bpms": []})

                elif "/get_chats" in path:
                    chats = {}
                    all_chats = self.database.chats.find_one({"name": "CHATS_NAMES_IDS"})
                    user = self.database.accounts_details.find_one({"name": data["current_user"].lower()})
                    try:
                        chats_ids = user["chats_ids"]
                    except KeyError:
                        chats_ids = []
                    result_dict = {id_: all_chats[id_] for id_ in chats_ids if id_ in all_chats}
                    res_data = json.dumps(result_dict)

                elif "/send_message" in path:
                    print(self.web_socket.clients)
                    chat = self.database.chats.find_one({"id": data["id"]})
                    if chat:
                        # Update the chat document with the new field
                        now = datetime.now()
                        # Format the time to include milliseconds
                        formatted_time = now.strftime("%Y-%m-%d %H;%M;%S;%f")[:-3]
                        self.database.chats.update_one(
                            {"id": data["id"]},
                            {"$set": {str(formatted_time): f'{data["message"]}|{data["current_user"]}'}}
                        )
                        res_data = json.dumps({"sent": "true"})

                elif "/get_messages" in path:
                    chat = self.database.chats.find_one({"id": data["id"]})
                    items = list(chat.items())
                    filtered_items = items[3:]
                    # Convert the filtered items back to a dictionary
                    chat = dict(filtered_items)
                    res_data = json.dumps(chat)

                elif "/get_contacts" in path:
                    account = self.database.accounts_details.find_one({"name": data["current_user"].lower()})
                    res_data = json.dumps({"names": account["friends"]})

                elif "/add_chat_for_contact" in path:
                    check = self.database.chats.find_one({"id": str(data["chat_id"])})
                    if data["contact_name"] not in check["accounts"]:
                        self.database.chats.update_one({"id": str(data["chat_id"])},
                                                       {"$push": {"accounts": data["contact_name"]}})
                        res_data = json.dumps({"added": "true"})
                        self.database.accounts_details.update_one({"name": data["contact_name"].lower()},
                                                                  {"$push": {"chats_ids": data["chat_id"]}})
                    else:
                        res_data = json.dumps({"already_in": "true"})

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

    @staticmethod
    def get_chat_id(chats_ids):
        id_ = str(random.randint(1000000, 10000000))
        while id_ in chats_ids.keys():
            id_ = str(random.randint(1000000, 10000000))
        return id_

    @staticmethod
    def send_files(client_socket, path, status_code):
        type_ = path.split(".")[-1]
        try:
            with open(path[1:], 'rb') as file:
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


class Arduino:
    def __init__(self, DataBase, WebSocketInstance):
        self.database = DataBase
        self.WS = WebSocketInstance
        self.protocol = Protocol()

    def start_arduino(self, approved_users):
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
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, approved_users))
                client_handler.start()

        except KeyboardInterrupt:
            print("[STOPPING] Server is stopping")
        finally:
            self.protocol.close()

    def handle_client(self, client_socket, approved_users):
        while True:
            # try:
            method, data = client_socket.get_msg().decode().split(":")
            if client_socket in approved_users.keys():
                if method == "bpm":
                    username, bpm = data.split(",")
                    today = date.today()
                    result = self.database.bpms.find_one({"name": username.lower()})
                    if result is None:
                        self.database.bpms.insert_one(
                            {"name": username.lower(), })
                    self.database.bpms.update_one({"name": username.lower()},
                                                  {"$push": {str(today): bpm}})
                    print("Today's date:", today)
            elif "confirm_ip" in method:
                print("confirm_ip")
                print(data)
                username, random_str = data.split(",")
                print(random_str, self.WS.randomStr)
                if random_str in self.WS.randomStr:
                    client_socket.send_msg("Success")
                    approved_users[client_socket] = username
                    print("Success")
                else:
                    client_socket.send_msg("Failure")
                    print("Failure")


class WebSocket(Web_Socket):
    def __init__(self):
        super().__init__()
        self.clients = {}
        self.randomStr = None

    def handle_client(self, client_socket, addr):
        self.accept_connection(client_socket)
        client_name = self.receive_data(client_socket)
        self.clients[client_name] = client_socket
        while True:
            try:
                data = self.receive_data(client_socket)
                # if data.split(' ')[0] in self.clients.keys():
                #     self.send_data(self.clients[data.split(' ')[0]], data)
                print("Received from client:", data)
                if "random_str" in data:
                    self.randomStr = data.split(":")[-1]
            except Exception as e:  # there's 3 different exceptions
                print(e)
                print(f"the client {addr} disconnected")
                keys_to_remove = [k for k, v in self.clients.items() if v == client_socket]
                for key in keys_to_remove:
                    del self.clients[key]
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
        self.web_socket = WebSocket()
        self.web_server = WebServer(self.DataBase, self.web_socket)
        self.arduino = Arduino(self.DataBase, self.web_socket)
        self.approved_users = {}

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
        arduino_thread = threading.Thread(target=self.arduino.start_arduino, args=(self.approved_users,), daemon=True)
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
