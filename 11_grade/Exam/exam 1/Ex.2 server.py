import socket

s = socket.socket()
s.bind(("127.0.0.1", 8820))
s.listen()
s.accept()

print("client accepted in server")