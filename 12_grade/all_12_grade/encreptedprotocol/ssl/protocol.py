from __future__ import annotations
import socket
from time import sleep

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Generate DH parameters (shared between client and server)
parameters = dh.generate_parameters(generator=2, key_size=512)  # Increase key size for security

# Encryption/Decryption settings
BLOCK_SIZE = AES.block_size

def generate_dh_keys():
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_key(private_key, peer_public_key_bytes):
    peer_public_key = serialization.load_pem_public_key(peer_public_key_bytes)
    shared_key = private_key.exchange(peer_public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=16,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    return derived_key

def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), BLOCK_SIZE))
    return iv + ct_bytes  # Prepend IV for decryption

def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:BLOCK_SIZE]  # Extract IV from the start
    ct = encrypted_message[BLOCK_SIZE:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
    return pt.decode('utf-8')

class Protocol:
    def __init__(self, sock=socket.socket(), is_client=True):
        self.LENGTH_FIELD_SIZE = 10
        self.socket = sock
        self.shared_key = None
        self.is_client = is_client

    def connect(self, addr: (str, int)):
        print("Connecting to server...")
        self.socket.connect(addr)
        self.dh_handshake()

    def settimeout(self, value):
        self.socket.settimeout(value)

    def bind(self, addr: (str, int)):
        self.socket.bind(addr)

    def listen(self):
        self.socket.listen()

    def close(self):
        self.socket.close()

    def accept(self):
        sock, addr = self.socket.accept()
        protocol = Protocol(sock, is_client=False)
        protocol.dh_handshake()
        return protocol, addr

    def recv_all(self, counter) -> bytes:
        msg = b""
        while len(msg) != counter:
            res = self.socket.recv(counter - len(msg))
            if res == b"":
                raise ConnectionError
            msg += res
        return msg

    def get_msg(self, timeout=None):
        self.socket.settimeout(timeout)
        length = self.recv_all(self.LENGTH_FIELD_SIZE)
        encrypted_msg = self.recv_all(int(length))

        return decrypt_message(encrypted_msg, self.shared_key)

    def send_msg(self, data):
        iv = get_random_bytes(16)
        if type(data) is str:
            data.encode()
        encrypted_msg = encrypt_message(data, self.shared_key, iv)
        try:
            self.socket.sendall(str(len(encrypted_msg)).zfill(self.LENGTH_FIELD_SIZE).encode() + encrypted_msg)
        except Exception:
            raise

    def dh_handshake(self):
        print("Starting DH handshake...")
        private_key, public_key = generate_dh_keys()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        print("Generated private key:", private_key)
        print("Generated public key:", public_key)
        print("Public key bytes:", public_key_bytes)

        if self.is_client:
            # Act as client
            print("Client sending public key...")
            self.socket.send(public_key_bytes)
            peer_public_key_bytes = self.socket.recv(1024)
        else:
            # Act as server
            print("Server receiving public key...")
            peer_public_key_bytes = self.socket.recv(1024)
            print("Received peer's public key bytes:", peer_public_key_bytes)

            print("Server sending public key...")
            self.socket.send(public_key_bytes)

        print("Deriving shared key...")
        try:
            self.shared_key = derive_shared_key(private_key, peer_public_key_bytes)
        except Exception as e:
            print("Error deriving shared key:", e)
            raise
        print("Shared key:", self.shared_key)
        print("DH handshake complete.")

# Adjusted key size and encoding/decoding where necessary

# Example usage:
# server_protocol = Protocol()
# server_protocol.bind(('localhost', 65432))
# server_protocol.listen()
# conn, addr = server_protocol.accept()
# conn.dh_handshake()
# conn.send_msg("Hello, client!")
# data = conn.get_msg()
# print("Received message from client:", data)

# client_protocol = Protocol(is_client=True)
# client_protocol.connect(('localhost', 65432))
# client_protocol.dh_handshake()
# data = client_protocol.get_msg()
# print("Received message from server:", data)
# client_protocol.send_msg("Hello, server!")
