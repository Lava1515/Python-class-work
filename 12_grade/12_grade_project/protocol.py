from Crypto.Random import get_random_bytes
import socket
import ssl


class Protocol:
    def __init__(self, sock=None, is_server=False, certfile=None, keyfile=None):

        self.LENGTH_FIELD_SIZE = 10
        self.socket = socket.socket() if sock is None else sock
        self.ssl_socket = None
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER if is_server else ssl.PROTOCOL_TLS_CLIENT)
        if is_server:
            if certfile is None or keyfile is None:
                raise ValueError("Server requires certfile and keyfile")
            self.context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        else:
            self.context.check_hostname = False
            self.context.verify_mode = ssl.CERT_NONE
        self.key = get_random_bytes(16)

    def connect(self, addr: (str, int)):
        self.ssl_socket = self.context.wrap_socket(self.socket, server_hostname=addr[0])
        return self.ssl_socket.connect(addr)

    def settimeout(self, value):
        return self.ssl_socket.settimeout(value) if self.ssl_socket else self.socket.settimeout(value)

    def bind(self, addr: (str, int)):
        return self.socket.bind(addr)

    def listen(self):
        return self.socket.listen()

    def close(self):
        if self.ssl_socket:
            self.ssl_socket.close()
        else:
            self.socket.close()

    def accept(self):
        sock, addr = self.socket.accept()
        ssl_sock = self.context.wrap_socket(sock, server_side=True)
        return Protocol(sock=ssl_sock), addr

    def recv_all(self, counter) -> bytes:
        msg = b""
        while len(msg) != counter:
            res = self.ssl_socket.recv(counter - len(msg)) if self.ssl_socket else self.socket.recv(counter - len(msg))
            if res == b"":
                print("recv None")
                raise ConnectionError
            msg += res
        return msg

    def get_msg(self, timeout=None):
        self.settimeout(timeout)
        length = int(self.recv_all(self.LENGTH_FIELD_SIZE))
        data = self.recv_all(length)

        return data

    def send_msg(self, data):
        try:
            if isinstance(data, str):
                data = data.encode()  # Ensure data is in bytes
            if self.ssl_socket:
                self.ssl_socket.sendall(
                    str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode() + data)
            else:
                self.socket.sendall(str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode() + data)
        except Exception as e:
            print(f"Error in send_msg: {e}")
            raise