import os
import socket

# http://127.0.0.1:80/calculate-next?num=15"
# http://127.0.0.1:80/index.html
# http://127.0.0.1:80/C:/Users/liavk/PycharmProjects/PYthonEX4/4.4/nfile.txt
# http://127.0.0.1:80/calculate-next


class Server:
    path = "/PYthonEX4/4.4/webroot/"
    typ_dict = {"html": "text/html; charset=utf-8",
                "txt": "text/html; charset=utf-8",
                "jpg": "image/jpeg",
                "js": "text/javascript; charset=UTF-8",
                "css": "text/css",
                "ico": "image/x-icon",
                "gif": "image/gif"}

    def __init__(self):
        self.server_socket = socket.socket()
        self.client_sock = None
        self.server_socket.bind(("0.0.0.0", 80))
        self.server_socket.listen()
        print("Server is up and running")

    def accept(self):
        (self.client_sock, client_address) = self.server_socket.accept()
        print("[Server]: New Connection From: '%s:%s'" % (client_address[0], client_address[1]))

    def get_message(self) -> tuple[bool, str]:
        data = self.client_sock.recv(1024)
        while len(data) > 0:
            data1 = data.decode().split("\r\n")
            params = data1[0].split()
            params[1] = params[1].replace("\\", "/")
            if params[0] == "GET" and params[1][0] == "/" and "HTTP/1.1" == params[2]:
                if params[1] != "/":
                    url = params[1][1:]
                    file = url.split("?")[0]

                    if file == "calculate-next":
                        num = url.split("=")[-1]
                        if num.isnumeric():
                            return True, f"{file}|{str(int(num)+1)}"
                        else:
                            return True, "not a number"


                    else:
                        if Server.check_is_file(file):
                            return True, file
                        file = Server.path + file

                        if Server.check_is_file(file):
                            return True, file

                        else:
                            print(file)
                            return False, "404 NOT A FILE"
                else:
                    return True, "/"

            data = self.client_sock.recv(1024)
        return False, "/"

    def close_client(self):
        self.client_sock.close()

    @staticmethod
    def check_is_file(file: str) -> bool:
        if os.path.isfile(file):
            return True
        else:
            return False

    def server_response(self, ok: bool, file: str) -> bytes:
        data = file.split("|")[-1]
        file = file.split("|")[0]
        if ok:
            if file == '/':
                file = Server.path + "index.html"
            typ_name = file.split(".")[-1]
            typ_name = typ_name.split("/")[-1]

            if data.split(".")[-1] in Server.typ_dict:
                typ = Server.typ_dict[typ_name]
                http = "HTTP/1.1 200 OK\r\n"
                if file != '/':
                    with open(file, 'rb') as file_N:
                        response = file_N.read()
                    length = "Content-Length: " + str(len(response)) + "\r\n"
                    msg = (http + length + "Content-Type: " + typ + "\r\n\r\n").encode() + response
                    return msg
            else:
                return data.encode()

        else:
            return b'"Error 404"'

    def Send(self, ok: bool, file: str):
        if ok:
            msg = self.server_response(ok, file)
            self.client_sock.send(msg)

        else:
            msg = self.server_response(ok, file)
            self.client_sock.send(msg)
            self.close_client()
        print("client left")



def main():
    myserver = Server()
    while True:
        myserver.accept()
        ok, file = myserver.get_message()
        myserver.Send(ok, file)


if __name__ == '__main__':
    main()
