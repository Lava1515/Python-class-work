#   Ex. 2.7 template - protocol
import socket


class Protocol:
    def __init__(self):
        self.command_list = ["DIR", "DELETE", "COPY", "EXECUTE", "TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT", "COMMANDS",
                             "UPGRADE"]
        self.LENGTH_FIELD_SIZE = 7
        self.PORT = 8820

    def check_cmd(self, data: str) -> bool:
        if data in self.command_list:
            return True
        else:
            return False

    def create_msg(self, data: bytes) -> bytes:
        length = str(len(data))
        zfill_length = (str(len(length)) + length).zfill(self.LENGTH_FIELD_SIZE)
        data = str(zfill_length).encode() + data
        return data

    def get_msg(self, my_socket: socket.socket) -> tuple[bool, bytes]:

        length = my_socket.recv(self.LENGTH_FIELD_SIZE).decode()
        if length.isdigit():
            message = my_socket.recv(int(length))
            while length < "":
                message = my_socket.recv(int(length))
                length -= len(message)

            return True, message
        elif length == "":
            return True, b""
        else:
            return False, b""
