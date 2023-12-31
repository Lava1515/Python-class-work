#   Ex. 2.7 template - server side
#   Author: Liav kolet

import os
import pyautogui
import shutil
import subprocess
from Protocol import *
import glob
IP = '0.0.0.0'


class Server:
    def __init__(self):
        self.server_socket = socket.socket()
        self.client_sock = None

    def connect(self, ip, port):
        self.server_socket.bind((ip, port))

    def accept(self):

        self.server_socket.listen()
        print("Server is up and running")
        (self.client_sock, client_address) = self.server_socket.accept()
        print("[Server]: New Connection From: '%s:%s'" % (client_address[0], client_address[1]))

    @staticmethod
    def handle_client_request(cmd: str, params: str = None) -> bytes:
        if Protocol.check_cmd(Protocol(), cmd):
            if cmd == "DIR":
                if params.endswith("\\"):
                    files_list = glob.glob(params + "*.*")
                else:
                    files_list = glob.glob(params + "\\*.*")
                return "\n".join(files_list).encode()\

            elif cmd == "DELETE":
                if os.path.isfile(params):
                    os.remove(params)
                    not_the_removed_files = glob.glob("\\".join(os.path.abspath(__file__).split("\\")[:-1]) + "\\*.*")
                    return "\n".join(not_the_removed_files).encode()
                else:
                    return "file doesn't exist".encode()

            elif cmd == "COPY":
                if os.path.isfile(params.split("|")[0]):
                    shutil.copy(params.split("|")[0], params.split("|")[1])
                    return "FILE copied successfully".encode()
                else:
                    return "file doesn't exist".encode()
            elif cmd == "EXECUTE":
                try:
                    subprocess.call(params)
                    return "The file have been EXECUTED ".encode()
                except (FileNotFoundError, OSError) as error:
                    return "The cant be opened (Doesn't exist or not .exe)".encode()

            elif cmd == "TAKE_SCREENSHOT":
                print("taking screenshot")
                image = pyautogui.screenshot()
                image.save(r'screen.jpg')
                return "The screen shot has been taken".encode()

            elif cmd == "SEND_PHOTO":
                with open(r'screen.jpg', "rb") as file:
                    photo_data = file.read()
                return photo_data

            elif cmd == "COMMANDS":
                return "DIR\nDELETE\nCOPY\nEXECUTE\nTAKE_SCREENSHOT\nSEND_PHOTO\nEXIT\ncommands".encode()

            elif cmd == "UPGRADE":
                return __file__
            #todo upgraed
        else:
            return b""

    def do_loop(self):
        while True:
            valid_protocol, msg = Protocol.get_msg(Protocol(), self.client_sock)
            msg = msg.decode()
            cmd = msg.split("|")[0]
            msg = "|".join(msg.split("|")[1:])

            if valid_protocol:
                print("[Client]: " + cmd + msg)
                if cmd == "TAKE_SCREENSHOT" or cmd == "SEND_PHOTO" or cmd == "commands":
                    reply = self.handle_client_request(cmd)

                    if reply is not None:
                        self.client_sock.send(Protocol.create_msg(Protocol(), reply))

                elif cmd != "EXIT":
                    reply = self.handle_client_request(cmd, msg)

                    if reply is not None:
                        self.client_sock.send(Protocol.create_msg(Protocol(), reply))

                else:
                    break

            elif msg == "":
                break

            else:
                response = 'Packet not according to protocol'
                print(response)
                self.client_sock.recv(1024)
        print("Closing connection")
        self.server_socket.close()


def main():
    server_sock = Server()
    server_sock.connect(IP, 8820)
    server_sock.accept()
    server_sock.do_loop()


if __name__ == '__main__':
    main()
