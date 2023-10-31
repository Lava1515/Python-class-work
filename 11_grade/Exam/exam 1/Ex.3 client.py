import socket

socket = socket.socket()
socket.connect(("127.0.0.3", 2000))

print("client connected")