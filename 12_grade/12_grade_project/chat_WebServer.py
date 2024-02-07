from datetime import datetime
import random
import socket
import json
import threading

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


class ChatServer:
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

                elif '/get_messages' in path:
                    chat_id = path.split('?')[1].split('=')[1] if '?' in path else 'default'
                    self.load_chat_messages(chat_id)
                    chat_messages = self.chats.get(chat_id, [])
                    data = json.dumps(chat_messages)
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(data))
                                     + "\r\n\r\n" + data)

                elif '/get_chats' in path:
                    name = path.split("?")[-1]
                    try:
                        with open(f"./chats_ids/{name}_chat_ids.json", 'r') as file:
                            chats_data = json.dumps(json.load(file))
                            self.response = (HTTP + STATUS_CODES["ok"]
                                             + CONTENT_TYPE + FILE_TYPE["json"]
                                             + CONTENT_LENGTH + str(len(chats_data))
                                             + "\r\n\r\n" + chats_data)
                    except Exception as e:
                        print(e)
                        with open(f"./chats_ids/{name}_chat_ids.json", 'w') as file_:
                            json.dump({}, file_)

                elif path != "/" and "?" not in path:
                    self.send_response(client_socket, path, "ok")

            elif 'POST' in method:
                if '/send_messages' in path:
                    message = json.loads(data)
                    chat_id = message["chat_id"]
                    if chat_id not in self.chats:
                        self.chats[chat_id] = []
                    message_number = len(self.chats[chat_id]) + 1
                    self.chats[chat_id].append({'number': message_number, 'content': message['content']})
                    self.update_messages_file(chat_id)
                    res_data = json.dumps({"success": "true"})
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

                    with open(f"./chats_ids/{message['current_user']}_chat_ids.json", 'r') as file:
                        try:
                            id_database = json.load(file)
                        except Exception as e:
                            print(e)
                            id_database = {}
                    id_database[chat_id]["time"] = str(datetime.now())
                    with open(f"./chats_ids/{message['current_user']}_chat_ids.json", 'w') as file_:
                        json.dump(id_database, file_)

                elif "get_id" in path:
                    check_chat = json.loads(data)
                    chat_name = check_chat["chat_name"]
                    id_ = random.randint(1000000, 10000000)
                    with open(f"./chats_ids/{check_chat['current_user']}_chat_ids.json", 'r') as file:
                        try:
                            id_database = json.load(file)
                        except json.decoder.JSONDecodeError:
                            id_database = {}
                    print(id_database)
                    while id_ in id_database:
                        id_ = random.randint(1000000, 10000000)
                    id_database[id_] = {"chat_name": chat_name, "time": str(datetime.now())}
                    with open(f'./chats_ids/{check_chat["current_user"]}_chat_ids.json', 'w') as file_:
                        json.dump(id_database, file_)
                    res_data = json.dumps({"the_id": str(id_)})
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

                elif "/send_details_Login" in path:
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

                elif "/add_friend" in path:
                    message = json.loads(data)
                    res_data = json.dumps({"Add_successfully": "false"})
                    try:
                        with open("accounts_details.json", 'r') as file:
                            details_ = json.load(file)
                    except Exception as e:
                        print(e)
                        with open("accounts_details.json", 'w') as file_:
                            details_ = {}
                            json.dump({}, file_)
                    current_user = message["current_user"].lower()
                    user_to_add = message["user_to_add"].lower()
                    if user_to_add in details_.keys():
                        try:
                            if current_user != user_to_add and user_to_add not in details_[current_user]["contacts"]:
                                details_[current_user]["contacts"].append(user_to_add)
                                res_data = json.dumps({"Add_successfully": "true"})
                            else:
                                print("cant add yourself")
                        except Exception as e:
                            print(e)
                            details_[current_user]["contacts"] = [user_to_add]
                            print(details_)
                        with open("accounts_details.json", 'w') as file_:
                            json.dump(details_, file_)
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)
                elif "/scrible" in path:
                    print(data)
                    res_data = ("")
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
        path = "webroot" + path
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


if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()
