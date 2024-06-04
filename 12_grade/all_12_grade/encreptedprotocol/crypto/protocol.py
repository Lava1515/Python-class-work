from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
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

        # Decrypt the received data
        # decrypted_data = self.decrypt(data)  # No need to skip the IV, it's handled in decrypt

        return data

    def send_msg(self, data):
        try:
            if isinstance(data, str):
                data = data.encode()  # Ensure data is in bytes

            # Encrypt the data before sending
            # encrypted_data = self.encrypt(data)

            if self.ssl_socket:
                # Send the length of the encrypted_data (including the IV)
                self.ssl_socket.sendall(
                    str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode() + data)
            else:
                self.socket.sendall(str(len(data)).zfill(self.LENGTH_FIELD_SIZE).encode() + data)
        except Exception as e:
            print(f"Error in send_msg: {e}")
            raise

    # def encrypt(self, data):
    #     iv = get_random_bytes(16)
    #     print("self.keiiiiiii", self.key)
    #     cipher = AES.new(b'1234567890123456', AES.MODE_CBC, iv)
    #     padded_data = pad(data, AES.block_size)
    #     encrypted_data = cipher.encrypt(padded_data)
    #     print(iv, " iv 1")
    #     print(encrypted_data, "encrypted_dat ")
    #     return iv + encrypted_data
    #
    # def decrypt(self, encrypted_data):
    #     iv = encrypted_data[:16]
    #     print(iv, " iv 2 ")
    #     actual_encrypted_data = encrypted_data[16:]
    #     print(actual_encrypted_data, " data")
    #     print("self.keyyyyyyyyyyyy", self.key)
    #     cipher = AES.new(b'1234567890123456', AES.MODE_CBC, iv)
    #     decrypted_data = cipher.decrypt(actual_encrypted_data)
    #     print(decrypted_data, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #     original_data = unpad(decrypted_data, AES.block_size)
    #     return original_data
