import socket

s = socket.socket()
s.bind("200000, 127.0.0.0")
s.listen()
s.accept()

print("client accepted in server")