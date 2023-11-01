from protocol import Protocol
import json


class Client:
    def __init__(self):
        self.socket = Protocol()

    def connect(self, ip, port):
        self.socket.connect((ip, port))

    def disconnect(self):
        self.socket.close()
        print("The client have been disconnected")


def main():
    my_client = Client()
    my_client.connect('127.0.0.1', 8820)


if __name__ == '__main__':
    main()
