import socket
import json
import threading


class ChatServer:
    def __init__(self):
        self.server_socket = None
        self.chats = {}
        self.clients = set()
        self.response = ""

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
            request = client_socket.recv(1024).decode('utf-8')

            method, path, *_ = request.split()
            print("the path", path)
            if "GET" in method and path == '/':
                path = "/index.html"
                self.send_html_response(client_socket, path)

            elif 'GET' in method and '/messages' in path:
                chat_id = path.split('?')[1].split('=')[1] if '?' in path else 'default'
                self.load_chat_messages(chat_id)
                chat_messages = self.chats.get(chat_id, [])
                self.response = f"HTTP/1.1 200 OK\r\nContent-type: application/json\r\n\r\n{json.dumps(chat_messages)}"

            elif 'POST' in method and '/messages' in path:
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

                self.response = "HTTP/1.1 200 OK\r\nContent-type: application/json\r\n\r\n{'success': true}"

            else:
                self.response = "HTTP/1.1 404 Not Found\r\n\r\n"
        finally:
            client_socket.send(self.response.encode('utf-8'))
            client_socket.close()
            self.clients.remove(client_socket)

    def broadcast_new_messages(self, chat_id, new_message):
        for client in self.clients:
            if client != self.server_socket:
                try:
                    client.send(f"New message in chat '{chat_id}': {new_message['content']}".encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting message to a client: {e}")

    def update_messages_file(self, chat_id):
        filename = f'{chat_id}_messages.json'
        with open(filename, 'w') as file:
            json.dump(self.chats[chat_id], file)

    def send_html_response(self, client_socket, path):
        path = "webroot/" + path.replace("/", "")
        try:
            with open(path, 'r') as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n{content}"
                client_socket.send(response.encode('utf-8'))
        except FileNotFoundError as e:
            print(e)
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            client_socket.send(response.encode('utf-8'))

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
