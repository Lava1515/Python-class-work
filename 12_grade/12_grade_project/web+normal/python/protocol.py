from __future__ import annotations
import socket


class Protocol:
    def __init__(self, sock=socket.socket()):
        self.LENGTH_FIELD_SIZE = 10
        self.socket = sock

    def connect(self, addr: (str, int)):
        return self.socket.connect(addr)

    def settimeout(self, value):
        return self.socket.settimeout(value)

    def bind(self, addr: (str, int)):
        return self.socket.bind(addr)

    def listen(self):
        return self.socket.listen()

    def close(self):
        self.socket.close()

    def accept(self):
        sock, addr = self.socket.accept()
        return Protocol(sock), addr

    def recv_all(self, counter) -> bytes:
        msg = b""
        while len(msg) != counter:
            res = self.socket.recv(counter - len(msg))
            if res == b"":
                print("recv None")
                raise ConnectionError
            msg += res
        return msg

    def get_msg(self, timeout=None):

        self.socket.settimeout(timeout)
        length = self.recv_all(self.LENGTH_FIELD_SIZE)
        return self.recv_all(int(length))

    def send_msg(self, data: bytes):
        try:
            self.socket.sendall(str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode() + data)
        except Exception:
            raise
