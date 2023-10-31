import socket

socket = socket.socket()
socket.bind(("127.0.0.3", 2000))


while True:
    socket.accept()
    continue

print("client accepted in server")