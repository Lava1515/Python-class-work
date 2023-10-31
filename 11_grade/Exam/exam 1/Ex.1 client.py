import socket

s = socket.socket()
s.connect((200000, "127.0.0,0"))

print("client connected")