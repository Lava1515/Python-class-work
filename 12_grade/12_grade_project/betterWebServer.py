import json
import os
import socket
import threading
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from inspect import signature
from pathlib import Path
from typing import Callable, Dict, DefaultDict

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from WebSockets import Web_Socket

import constans


@dataclass
class Response:
    CONTENT_TYPE: str
    STATUS_CODE: str


@dataclass
class Request:
    URI: str


class Database:
    _instance: "Database" = None

    def __init__(self):
        if not Database._instance:
            uri = "mongodb+srv://lavak:Lava@heartrate.qduwqzq.mongodb.net/?retryWrites=true&w=majority&appName=heartrate"
            # Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))
            self._database = client.heartrate  # access database
            Database._instance = self

    @property
    def database(self):
        if not self._instance:
            Database()
        return self._instance._database


def get_database():
    return Database().database


class WebServer:
    def __init__(self) -> None:
        self.server_socket = None
        self._mapping: DefaultDict[str, Dict[str, Callable]] = defaultdict(dict)
        self._folder_mappings: Dict[str, Callable] = {}
        self.web_socket = None

    def run(self, client_socket):
        try:
            client_request = client_socket.recv(1024).decode()
            data = client_request.split("\r\n\r\n")[-1]
            method, path, *_ = client_request.split()
            if not path:
                path = "/"
            if self.file_exists_in_directory("/webroot", path):
                path = f"/webroot/{path}"

            handler: Callable = self._mapping.get(method.upper(), {}).get(path, None)

            if not handler:
                for mounted_folder, folder_handler in self._folder_mappings.items():
                    if path.startswith(mounted_folder):
                        handler = folder_handler
                        break

                if not handler:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n"
                    client_socket.send(response.encode())
                    return

            request = Request(path)
            response = Response(constans.FILE_TYPE["json"], constans.STATUS_CODES["ok"])

            args = [data]
            handler_signature = signature(handler).parameters
            for parameter, param_type in list(handler_signature.items())[1:]:
                if param_type.annotation == Web_Socket:
                    args.append(self.web_socket)
                elif param_type.annotation == Response:
                    args.append(response)
                elif param_type.annotation == Request:
                    args.append(request)
                elif param_type.annotation == param_type.empty:
                    args.append(None)
                else:
                    args.append(param_type.annotation())

            res_data = handler(*args)

            res = (
                    constans.HTTP + response.STATUS_CODE +
                    constans.CONTENT_TYPE + response.CONTENT_TYPE +
                    constans.CONTENT_LENGTH + str(len(res_data)) +
                    "\r\n\r\n"
            )
            if type(res_data) is str:
                res += res_data
            res = res.encode()
            if type(res_data) is bytes:
                res += res_data
            client_socket.send(res)
        finally:
            client_socket.close()

    def post(self, route: str) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self._mapping["POST"][route] = func
            return func

        return wrapper

    def get(self, route: str) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self._mapping["GET"][route] = func
            return func

        return wrapper

    def mount_folder(self, base_route: str) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self._folder_mappings[base_route] = func
            return func

        return wrapper

    @staticmethod
    def file_exists_in_directory(directory, filename):
        # Ensure the filename does not start with a slash
        filename = filename.lstrip('/')
        # Join the directory and filename, then replace backslashes with forward slashes
        file_path = "."+os.path.join(directory, filename).replace('\\', '/')

        return os.path.isfile(file_path)

    def start_server(self, web_socket):
        self.web_socket = web_socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 5000))
        self.server_socket.listen(5)
        print("Register as an Admin http://127.0.0.1:5000/AdminRegister.html")
        print("Server is running on http://127.0.0.1:5000")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                client_handler = threading.Thread(target=self.run, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            self.server_socket.close()


web_server = WebServer()


@web_server.get("/")
def login(data, response: Response):
    path = Path("webroot/Login.html")
    response.CONTENT_TYPE = "text/html\r\n"
    return path.read_text()


@web_server.mount_folder("/webroot")
def get_web_files(data, response: Response, request: Request):
    uri = request.URI[1:] if request.URI.startswith("/") else request.URI
    path = Path(uri).absolute()
    if not path.exists():
        response.STATUS_CODE = constans.STATUS_CODES["not found"]
        return ""
    response.CONTENT_TYPE = constans.FILE_TYPE[path.suffix[1:]]
    return path.read_bytes()


@web_server.get("/get_coaches")
def get_coaches(data, response: Response, database: get_database):
    names = database.accounts_details.find({"Permissions": "Coach"})
    namelist = [name["name"].lower() for name in names]
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return json.dumps(namelist)


@web_server.post("/send_details_Login")
def send_details_login(data, response: Response, database: get_database):
    data = json.loads(data)
    result = database.accounts_details.find_one({"name": data["name"].lower()})
    res_data = json.dumps({"can_login": "false"})
    if result is not None and result["password"] == data["pass"]:
        res_data = json.dumps({"can_login": "true"})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/send_details_Register")
def send_details_register(data, response: Response, database: get_database):
    data = json.loads(data)
    result = database.accounts_details.find_one({"name": data["name"].lower()})
    if result is None:
        database.accounts_details.insert_one(
            {"name": data["name"].lower(), "password": data["pass"], "Permissions": "Trainer"})
        res_data = json.dumps({"existing": "false"})
    else:
        res_data = json.dumps({"existing": "true"})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/AdminRegister")
def admin_register(data, response: Response, database: get_database):
    data = json.loads(data)
    all_names = database.accounts_details.find_one({"name": data["name"].lower()})
    if all_names is None:
        database.accounts_details.insert_one(
            {"name": data["name"].lower(), "password": data["pass"], "Permissions": "Coach"})
        res_data = json.dumps({"existing": "false"})
    else:
        res_data = json.dumps({"existing": "true"})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/add_contact")
def add_contact(data, response: Response, database: get_database):
    data = json.loads(data)
    friend_name = data["data"].lower()
    current_user_name = data["current_user"].lower()

    # Check if the friend exists in the database
    friend = database.accounts_details.find_one({"name": friend_name})
    if friend:
        # Check if the current user exists in the database
        user = database.accounts_details.find_one({"name": current_user_name})
        if user:
            # Check if the friend already exists for the user
            if friend_name in user.get("friends", []):
                res_data = json.dumps({"existing": True})
            else:
                # Add the friend to the user's friends list
                database.accounts_details.update_one({"name": current_user_name.lower()},
                                                     {"$push": {"friends": friend_name}})
                res_data = json.dumps({"existing": False})
        else:
            res_data = json.dumps({"error": "User not found"})
    else:
        res_data = json.dumps({"error": "Contact not found"})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/create_group")
def create_group(data, response: Response, database: get_database):
    data = json.loads(data)
    chats = database.chats.find_one({"name": "CHATS_NAMES_IDS"})
    if chats is None:
        database.chats.insert_one({"name": "CHATS_NAMES_IDS"})
        chats = database.chats.find_one({"name": "CHATS_NAMES_IDS"})

    id_ = len(chats)  # Dummy function to simulate chat ID generation
    database.chats.insert_one({"id": str(id_), "accounts": [data["data"].lower()]})
    database.chats.update_one({"name": "CHATS_NAMES_IDS"},
                              {"$set": {str(id_): data["data"]}})
    database.accounts_details.update_one({"name": data["current_user"].lower()},
                                         {"$push": {"chats_ids": str(id_)}})
    res_data = json.dumps({"added_chat": "true", "id": str(id_)})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/SetCoach")
def set_coach(data, response: Response, database: get_database):
    data = json.loads(data)
    coach_name = data["coach"].lower()
    current_user_name = data["current_user"].lower()

    # Check if coach exists
    coach = database.accounts_details.find_one({"name": coach_name, "Permissions": "Coach"})
    if coach:
        # Check if current user exists
        user = database.accounts_details.find_one({"name": current_user_name})
        if user:
            # Check if current user already has a coach
            if not user.get("coach"):
                # Update current user's coach and add current user to coach's trainers
                database.accounts_details.update_one(
                    {"name": current_user_name.lower()},
                    {"$set": {"coach": coach_name}}
                )
                database.accounts_details.update_one(
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
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_Permissions")
def get_permissions(data, response: Response, database: get_database):
    data = json.loads(data)
    account = database.accounts_details.find_one({"name": data["current_user"].lower()})
    res_data = json.dumps({"Permissions": account["Permissions"]})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_trainers")
def get_trainers(data, response: Response, database: get_database):
    data = json.loads(data)
    account = database.accounts_details.find_one({"name": data["current_user"].lower()})
    res_data = json.dumps({"Trainers": account["trainers"]})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_bpms_dates")
def get_bpms_dates(data, response: Response, database: get_database):
    data = json.loads(data)
    account = database.bpms.find_one({"name": data["current_user"].lower()})
    try:
        dates = list(filter(lambda key: str(key) != "_id" and key != "name", account.keys()))
        res_data = json.dumps({"dates": dates})
    except AttributeError:
        res_data = json.dumps({"dates": []})
        print("no dates saved")
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_date_bpms")
def get_date_bpms(data, response: Response, database: get_database):
    data = json.loads(data)
    account = database.bpms.find_one({"name": data["current_user"].lower()})
    try:
        res_data = json.dumps({"bpms": account[data["date"]]})
    except KeyError:
        res_data = json.dumps({"bpms": []})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_chats")
def get_chats(data, response: Response, database: get_database):
    data = json.loads(data)
    chats = {}
    all_chats = database.chats.find_one({"name": "CHATS_NAMES_IDS"})
    user = database.accounts_details.find_one({"name": data["current_user"].lower()})
    try:
        chats_ids = user["chats_ids"]
    except KeyError:
        chats_ids = []
    result_dict = {id_: all_chats[id_] for id_ in chats_ids if id_ in all_chats}
    res_data = json.dumps(result_dict)
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/send_message")
def send_message(data, WebSoket: Web_Socket, response: Response, database: get_database):
    res_data = ""
    data = json.loads(data)
    chat = database.chats.find_one({"id": data["id"]})
    if chat:
        users_in_chat_id = chat["accounts"]
        for user in users_in_chat_id:
            if user in WebSoket.clients.keys() and user != data["current_user"].lower():
                WebSoket.send_data(WebSoket.clients[user],
                                   f"Got message|msg_id:{data["id"]}|sender_name:{data["current_user"].lower()}|msg_data:{data["message"]}")

        # Update the chat document with the new field
        now = datetime.now()
        # Format the time to include milliseconds
        formatted_time = now.strftime("%Y-%m-%d %H;%M;%S;%f")[:-3]
        database.chats.update_one(
            {"id": data["id"]},
            {"$set": {str(formatted_time): f'{data["message"]}|{data["current_user"].lower()}'}}
        )
        res_data = json.dumps({"sent": "true"})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_messages")
def get_messages(data, response: Response, database: get_database):
    data = json.loads(data)
    chat = database.chats.find_one({"id": data["id"]})
    items = list(chat.items())
    filtered_items = items[3:]
    # Convert the filtered items back to a dictionary
    chat = dict(filtered_items)
    res_data = json.dumps(chat)
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/get_contacts")
def get_contacts(data, response: Response, database: get_database):
    data = json.loads(data)
    account = database.accounts_details.find_one({"name": data["current_user"].lower()})
    res_data = json.dumps({"names": account["friends"]})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


@web_server.post("/add_chat_for_contact")
def add_chat_for_contact(data, response: Response, database: get_database):
    data = json.loads(data)
    check = database.chats.find_one({"id": str(data["chat_id"])})
    if data["contact_name"] not in check["accounts"]:
        database.chats.update_one({"id": str(data["chat_id"])},
                                  {"$push": {"accounts": data["contact_name"]}})
        res_data = json.dumps({"added": "true"})
        database.accounts_details.update_one(
            {"name": data["contact_name"].lower()},
            {"$push": {"chats_ids": data["chat_id"]}}
        )
    else:
        res_data = json.dumps({"already_in": "true"})
    response.CONTENT_TYPE = constans.FILE_TYPE["json"]
    return res_data


