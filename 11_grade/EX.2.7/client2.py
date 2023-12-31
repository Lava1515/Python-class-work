#   Ex. 2.7 template - client side
#   Author: Liav kolet
import os
import socket
import pyautogui
from Protocol import *
import easygui

IP = '127.0.0.1'


def handle_server_response(my_socket: socket.socket, cmd: str):
    # (8) treat all responses except SEND_PHOTO
    if cmd != "SEND_PHOTO":
        return get_msg(my_socket)
    # (10) treat SEND_PHOTO
    else:
        ok, image_data = get_msg(my_socket)
        with open(r'save_screen.jpg', "wb") as file:
            file.write(image_data)
        os.startfile(r'save_screen.jpg')
        return ok, "The photo have been saved ".encode()


def main():
    # open socket with the server
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 8820))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if cmd == 'EXIT':
            break
        param = ""
        if cmd == "DIR":
            param = "|" + input("Pleas enter the DIR you want to list")
        elif cmd == "DELETE" or cmd == "EXECUTE":
            param = "|" + input("pleas enter the file you want to %s " % cmd)
        elif cmd == "COPY":
            param = "|" + input("pleas enter the file you want to copy ") + "|"
            param += input("pleas enter the path you want to copy to ")

        if check_cmd(cmd + param):
            packet = create_msg((cmd + param).encode())
            my_socket.send(packet)
            ok, data = handle_server_response(my_socket, cmd)
            if ok:
                print(data.decode())
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
