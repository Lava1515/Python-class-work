import os
import socket
from PIL import Image

# http://109.186.123.78:8820/index.html
# http://127.0.0.1:80/index.html

class Server:
    path = "C:/Users/liavk/PycharmProjects/EX.4/4.4/webroot"
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

    def get_message(self) -> tuple[bool, str | list[str] | bytes]:
        Data = self.client_sock.recv(1024)
        while len(Data) > 0:
            data1 = Data.decode().split("\r\n")
            params = data1[0].split()
            params[1] = params[1].replace("\\", "/")
            if (params[0] == "GET" or params[0] == "POST") and params[1][0] == "/" and "HTTP/1.1" == params[2]:
                if params[1] != "/":
                    url = params[1][1:]
                    file = url.split("?")[0]
                    if file == "calculate-next":
                        num = url.split("=")[-1]
                        if num.isnumeric():
                            return True, f"{file}|{str(int(num) + 1)}"
                        else:
                            return True, "not a number"

                    elif file == "calculate-area":
                        data = url.split("?")[-1]
                        height = data.split("&")[0]
                        width = data.split("&")[1]
                        height = height.split("=")[-1]
                        width = width.split("=")[-1]
                        s = (int(height) * int(width))/2
                        if height.isnumeric() and width.isnumeric():
                            return True, f"{file}|{str(int(s))}"
                        else:
                            return True, "not have a numbers"

                    elif file == "upload":
                        filename = url.split("=")[-1]
                        length = int((Data.split(b"Content-Length: ")[1]).split(b"\r\n")[0].strip())
                        data = b""
                        while length > len(data):
                            data += self.client_sock.recv(length - len(data))
                        with open(f"{filename}", "wb") as file:
                            file.write(data)

                        if not filename.endswith(".jpeg"):
                            im = Image.open(filename)
                            rgb_im = im.convert('RGB')
                            rgb_im.save(f'{".".join(filename.split(".")[:-1])}.jpeg')
                            os.remove(filename)
                            return True, [f'{".".join(filename.split(".")[:-1])}.jpeg']
                        else:
                            return True , [filename]

                    elif file =="image":
                        name = url.split("=")[-1]
                        name = name + ".jpeg" if not name.endswith(".jpeg") else name
                        if os.path.isfile(name):
                            with open(name, "rb") as file:
                                photo_data = file.read()
                            return True, photo_data
                        else:
                            return False , "404 NOT A FILE"


                    else:
                        if Server.check_is_file(file):
                            return True, file
                        file = Server.path + file

                        if Server.check_is_file(file):
                            return True, file

                        else:
                            return False, "404 NOT A FILE"
                else:
                    return True, "/"

            Data = self.client_sock.recv(1024)
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
        http = "HTTP/1.1 200 OK\r\n"
        if isinstance(file, list):
            return (http + "\r\n" + file[0]).encode()

        if type(file) == bytes:
            length = "Content-Length: " + str(len(file)) + "\r\n"
            msg = (http + length + "Content-Type: " + "image/jpeg" + "\r\n\r\n").encode() + file
            return msg

        data = file.split("|")[-1]
        file = file.split("|")[0]
        if ok:
            if file == '/':
                file = Server.path + "index.html"
            typ_name = file.split(".")[-1]
            typ_name = typ_name.split("/")[-1]
            typ = Server.typ_dict[typ_name]
            if data.split(".")[-1] in Server.typ_dict:

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
            while msg != b"":
                send_a = self.client_sock.send(msg)
                msg = msg[send_a:]

        else:
            msg = self.server_response(ok, file)
            while msg != b"":
                send_a = self.client_sock.send(msg)
                msg = msg[send_a:]
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
