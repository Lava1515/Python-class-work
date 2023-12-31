import socket

socket = socket.socket()
socket.bind(("127.0.0.3", 2000))
socket.listen()


while True:
    socket.accept()
    print("client conacted")
    continue

print("client accepted in server")