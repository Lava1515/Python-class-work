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

    def read_file(self, file_name):
        """ Read A File """
        with open(file_name, "rb") as f:
            data = f.read()
        return data

    def load_chat_messages(self, chat_id):
        filename = f'{chat_id}_messages.json'
        try:
            with open(filename, 'r') as file:
                self.chats[chat_id] = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with numbering
            self.chats[chat_id] = [{'number': i + 1, 'content': f'Message {i + 1}'} for i in range(3)]
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
                    path = "/index.html"
                    self.send_response(client_socket, path, "ok")
                elif path != "/" and "?" not in path:
                    self.send_response(client_socket, path, "ok")
                if '/messages' in path:
                    chat_id = path.split('?')[1].split('=')[1] if '?' in path else 'default'
                    self.load_chat_messages(chat_id)
                    chat_messages = self.chats.get(chat_id, [])
                    data = json.dumps(chat_messages)
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(data))
                                     + "\r\n\r\n" + data)

            elif 'POST' in method:
                if '/messages' in path:
                    content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
                    content = "{" + request.split("{")[-1].split("}")[0] + "}"
                    print(f"Received content: {content}")
                    message = json.loads(content)
                    chat_id = message.get('chat_id', 'default')
                    if chat_id not in self.chats:
                        self.chats[chat_id] = []
                    message_number = len(self.chats[chat_id]) + 1
                    self.chats[chat_id].append({'number': message_number, 'content': message['content']})
                    self.update_messages_file(chat_id)
                    self.broadcast_new_messages(chat_id, message)
                    res_data = json.dumps({"success": "true"})
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len({res_data}))
                                     + "\r\n\r\n" + res_data)

                if "check_id" in path:
                    id_ = data.split(":")[-1].replace("}", "")
                    print(id)
                    with open("chat_ids.json", 'r') as file:
                        try:
                            id_database = json.load(file)
                        except json.decoder.JSONDecodeError:
                            id_database = {}
                    if id_ in id_database:
                        print("false")
                        print(json.dumps({"success": "false"}))
                        res_data = json.dumps({"success": "false"})
                        self.response = (HTTP + STATUS_CODES["ok"]
                                         + CONTENT_TYPE + FILE_TYPE["json"]
                                         + CONTENT_LENGTH + str(len(res_data))
                                         + "\r\n\r\n" + res_data)
                    else:
                        id_database[id_] = ""
                        with open("chat_ids.json", 'w') as file_:
                            print(id_)
                            json.dump(id_database, file_)

            else:
                self.response = "HTTP/1.1 404 Not Found\r\n\r\n"
        finally:
            client_socket.send(self.response.encode())
            client_socket.close()
            self.clients.remove(client_socket)

    def broadcast_new_messages(self, chat_id, new_message):
        for client in self.clients:
            if client != self.server_socket:
                try:
                    client.send(f"New message in chat '{chat_id}': {new_message['content']}".encode())
                except Exception as e:
                    print(f"Error broadcasting message to a client: {e}")

    def update_messages_file(self, chat_id):
        filename = f'{chat_id}_messages.json'
        with open(filename, 'w') as file:
            json.dump(self.chats[chat_id], file)

    @staticmethod
    def send_response(client_socket, path, status_code):
        type_ = path.split(".")[-1]
        print("origin", path)
        path = "webroot/" + path.replace("/", "")
        print("path", path)
        try:
            with open(path, 'r') as file:
                content = file.read()
                content_type = CONTENT_TYPE + FILE_TYPE[type_]
                content_length = CONTENT_LENGTH + str(len(content.encode())) + "\r\n"
                http_response = HTTP + STATUS_CODES[status_code] + content_type + content_length + "\r\n"
                http_response = http_response.encode() + content.encode()
                client_socket.send(http_response)
        except FileNotFoundError as e:
            print(e)
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            client_socket.send(response.encode())

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5000))
        self.server_socket.listen(5)
        print("Server is running on http://localhost:5000")

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
