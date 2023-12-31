"""
------------------
    Server.py
------------------
    implements 2 classes.

    the first of those is SC_Connection
        where sc stands for socket.
        basically, it holds a connection with a client

    the second one is Server, which is the main selling point in this file.
        that server uses the main_loop method in order to execute its commands.
        it can handle multiple clients by storing them in SC_Connections, and handling each of those

    completed methods: start, accept
"""

import socket
from Protocol import Protocol as p


class SC_Connection:
    def __init__(self, conn, addr):
        self.connection = conn
        self.address = addr


class Server:
    def __init__(self, host: str, port: int, number_of_clients: int):
        self.connections = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = host
        self.PORT = port
        self.number_of_clients = number_of_clients

    # starts the server
    def start(self):
        self.sock.bind((self.HOST, self.PORT))      # binds the socket

    # accept clients into the server
    def accept(self):
        connection, address = self.sock.accept()    # accepting the client
        self.connections.append(SC_Connection(connection, address))     # creating a SC_Connection,
        # and adding it to the list of clients

    # manage client
    def manage_single_client(self, client: SC_Connection):
        """
            this method is responsible for handling a connection with an individual client.
            data must be received via the protocol
        """

        data = ""   # need the protocol for receiving messages
        if data:
            # here comes your code
            print(f"data: {data}, connections: {len(self.connections)}")
        else:
            # the client sent a null
            print("disconnected")
            self.connections.remove(client)

    # main loop (main)
    def main_loop(self):
        self.start()    # start the server
        while True:
            self.sock.listen(self.number_of_clients)    # listen for new clients
            self.accept()   # if any, accept the new clients
            for connection in self.connections:     # for each of the current clients
                self.manage_single_client(connection)   # handle it

    def Get_client(self):
        """
            this method is responsible for letting the server know which
            client is currently connected \ handled
        """
        pass    # can check for a "prefix message",
        # a message that would inform you about the content of the next message

    def Handle_regular_ballotbox(self):
        """
            this method is responsible for handling a connection
            with a regular ballot box as the current client
        """
        pass

    def Handle_double_ballotbox(self):
        """
              this method is responsible for handling a connection
              with a double ballot box as the current client
        """
        pass

    def Handle_stopper(self):
        """
              this method is responsible for handling a connection
              with a stopper (chicken) as the current client
        """
        pass


if __name__ == "__main__":
    NUMBER_OF_CLIENTS = 3
    current = Server(p.HOST, p.PORT, NUMBER_OF_CLIENTS)
    current.main_loop()
