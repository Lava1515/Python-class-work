import socket
import threading
from datetime import date

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from WebSockets import Web_Socket  # ik know there is built in module
from betterWebServer import web_server
from generate_cert_and_key import check_and_generate_cert_and_key
from protocol import Protocol


class Arduino:
    def __init__(self, DataBase, WebSocketInstance):
        self.database = DataBase
        self.WS = WebSocketInstance
        self.certfile = 'certfile.pem'
        self.keyfile = 'keyfile.pem'
        check_and_generate_cert_and_key(self.certfile, self.keyfile)
        self.protocol = Protocol(is_server=True, certfile=self.certfile, keyfile=self.keyfile)

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
            method, data = client_socket.get_msg().decode().split(":")
            if client_socket in approved_users.keys():
                if method == "bpm":
                    username, bpm = data.split(",")
                    print(bpm)
                    today = date.today()
                    result = self.database.bpms.find_one({"name": username.lower()})
                    if result is None:
                        self.database.bpms.insert_one(
                            {"name": username.lower(), })
                    self.database.bpms.update_one({"name": username.lower()},
                                                  {"$push": {str(today): bpm}})
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
        self.clients[client_name.lower()] = client_socket
        while True:
            try:
                data = self.receive_data(client_socket)
                print(data)
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
        self.web_server = web_server
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
        print(self.web_socket)
        web_thread = threading.Thread(target=self.web_server.start_server, args=(self.web_socket,), daemon=True)
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
