from datetime import datetime
import threading
import random
import serial
import socket
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
        global point, dofek
        self.clients.add(client_socket)
        try:
            request = client_socket.recv(1024).decode()
            data = request.split("\r\n\r\n")[-1]
            method, path, *_ = request.split()
            if "GET" in method:
                if path == '/':
                    print("none")
                    path = "httpserver.html"
                    self.send_response(client_socket, path, "ok")
                elif path != "/":
                    print("path ", path)
                    path = "httpserver.js"
                    self.send_response(client_socket, path, "ok")
                elif "get_data" in path:
                    print("get_dataaagag")
                    print(dofek)
                    res_data = json.dumps(dofek)
                    self.response = (HTTP + STATUS_CODES["ok"]
                                     + CONTENT_TYPE + FILE_TYPE["json"]
                                     + CONTENT_LENGTH + str(len(res_data))
                                     + "\r\n\r\n" + res_data)

            elif 'POST' in method:
                pass
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
        try:
            with open(path, 'rb') as file:
                content = file.read()
                content_type = CONTENT_TYPE + FILE_TYPE[type_]
                content_length = CONTENT_LENGTH + str(len(content)) + "\r\n"
                http_response = HTTP + STATUS_CODES[status_code] + content_type + content_length + "\r\n"
                http_response = http_response.encode() + content
                client_socket.send(http_response)
                print("sent")

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


def arduino():
    global dofek
    # Define the serial port and baud rate
    serial_port = 'COM3'  # Change this to the appropriate port
    baud_rate = 9600

    # Connect to the Arduino board
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    try:
        while True:
            # Wait for a message from Arduino
            response = ser.readline().decode('utf-8').strip()
            if response:
                # if int(response) == 100100:
                #     response = 10000
                dofek = int(response) // 55.5 + 40
    finally:
        ser.close()  # Close the serial port when done


if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()
    t = threading.Thread(target=arduino, daemon=True)
    t.start()
    t.join()
