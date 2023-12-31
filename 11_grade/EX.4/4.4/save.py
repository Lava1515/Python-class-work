import socket

# http://127.0.0.1:80

class Server:
    def __init__(self):
        self.server_socket = socket.socket()
        self.client_sock = socket.socket()

    def connect(self):
        self.server_socket.bind(("0.0.0.0", 80))

    def accept(self):
        self.server_socket.listen()
        print("Server is up and running")
        (self.client_sock, client_address) = self.server_socket.accept()
        print("[Server]: New Connection From: '%s:%s'" % (client_address[0], client_address[1]))


def main():
    i = 0
    while True:
        server_sock = Server()
        server_sock.connect()
        server_sock.accept()
        data = "0"
        while len(data) > 0:
            data = server_sock.client_sock.recv(1024).decode()
            data = data.split("\n")
            if data[0][:3] != "GET" or data[0][3:5] != " /" or "HTTP/1.1" not in data[0]:
                print("not valid client ")
                break
            print()

        server_sock.client_sock.close()
        print("client left")
        i = i + 1


if __name__ == '__main__':
    main()
