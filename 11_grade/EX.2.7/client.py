#   Ex. 2.7 template - client side
#   Author: Liav kolet
import os
from Protocol import *


class Client:
    def __init__(self):
        self.my_socket = socket.socket()

    def connect(self, ip, port):
        self.my_socket.connect((ip, port))

    def do_loop(self) -> bool:
        cmd = input("Please enter command:\n")
        cmd = cmd.upper()
        if cmd == 'EXIT':
            self.my_socket.send("EXIT".encode())
            return False
        if Protocol.check_cmd(Protocol(), cmd):
            param = ""
            if cmd == "DIR":
                param = "|" + input("Pleas enter the DIR you want to list")
            elif cmd == "DELETE" or cmd == "EXECUTE":
                param = "|" + input("pleas enter the file you want to %s " % cmd)
            elif cmd == "COPY":
                param = "|" + input("pleas enter the file you want to copy ") + "|"
                param += input("pleas enter the path you want to copy to ")

            packet = Protocol.create_msg(Protocol(), (cmd + param).encode())
            self.my_socket.send(packet)
            ok, data = Client.handle_server_response(self.my_socket, cmd)
            if ok:
                print(data.decode())
        else:
            print("Not a valid command, or missing parameters\n")
        return True

    def disconnect(self):
        self.my_socket.close()
        print("The client have been disconnected")

    @staticmethod
    def handle_server_response(my_socket: socket.socket, cmd: str):
        if cmd != "SEND_PHOTO":
            return Protocol.get_msg(Protocol(), my_socket)
        else:
            ok, image_data = Protocol.get_msg(Protocol(), my_socket)
            with open(r'save_screen.jpg', "wb") as file:
                file.write(image_data)
            os.startfile(r'save_screen.jpg')
            return ok, "The photo have been saved ".encode()


def main():
    my_client = Client()
    my_client.connect('127.0.0.1', 8820)
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT\nCOMMANDS\nUPGRADE')
    while my_client.do_loop():
        continue

    Client.disconnect(Client())


if __name__ == '__main__':
    main()


