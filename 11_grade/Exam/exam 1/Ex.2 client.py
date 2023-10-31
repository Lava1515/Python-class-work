import socket

s = socket.socket()
s.connect(("127.0.0.1", 8820))

print("client connected")