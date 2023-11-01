import os
import json
import socket
import threading
import multiprocessing
from typing import Hashable

from protocol import Protocol


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.data_list = {}

    def set_value(self, key: Hashable, data):
        if os.path.isfile(self.filename) is False:
            raise Exception("File not found")
        try:
            with open(self.filename) as fp:
                self.data_list = json.load(fp)
        except Exception:
            pass
        # the file is Empty
        self.data_list.update({key: data})
        with open(self.filename, 'w') as json_file:
            json.dump(self.data_list, json_file,
                      indent=4,
                      separators=(',', ': '))

    def get_data(self, key: Hashable):
        try:
            with open(self.filename) as fp:
                self.data_list = json.load(fp)
        except Exception:
            print("the file is Empty")
        try:
            return self.data_list[key]
        except KeyError:
            return "The key you entered is not valid"

    def delete_value(self, key: Hashable):
        with open(self.filename) as fp:
            self.data_list = json.load(fp)

        if key in self.data_list:
            del self.data_list[key]
            print("The Deleted key is:", key)

        with open(self.filename, 'w') as json_file:
            json.dump(self.data_list, json_file,
                      indent=4,
                      separators=(',', ': '))


# DB = DataBase('data.json')
# DB.set_value("aaaddag", "hgjkhf")
# print(DB.get_data("aaag"))
# DB.delete_value("aaag")
#

class WriteData(DataBase):
    def __init__(self):
        super().__init__('data.json')
        self.lock_clients_sock = threading.Lock()

    def get_new_data(self):
        key = input("the key you want to add")
        data = input("the data you want to relate to the key")
        self.lock_clients_sock.acquire()
        self.set_value(key, data)
        self.lock_clients_sock.release()

    def remove_key(self):
        key = input("the key you want to remove")
        self.lock_clients_sock.acquire()
        self.delete_value(key)
        self.lock_clients_sock.release()


class Server:
    def __init__(self):
        self.clients_sock = {}
        self.server_socket = Protocol()
        self.lock_clients_sock = threading.Lock()

    def bind(self, ip, port):
        self.server_socket.bind((ip, port))

    def listen(self):
        self.server_socket.listen()
        print("Server is up and running")

    def accept(self):
        try:
            client_sock, client_address = self.server_socket.accept()
        except TimeoutError:
            return
        self.lock_clients_sock.acquire()
        self.clients_sock[client_sock] = client_address
        self.lock_clients_sock.release()
        print('\r' + "[Server]: New Connection From: '%s:%s'" % client_address)

    def hendle_cleints(self):
        pass


if __name__ == '__main__':
    server = Server()
    server.bind("0.0.0.0", 8820)
    server.listen()
    server.accept()
