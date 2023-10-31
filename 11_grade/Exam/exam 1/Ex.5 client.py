import socket

for i in range(5):
    s = socket.socket()
    s.connect(("127.0.0.5", 2000))
    s.send(str(i).encode())
    print("client connected")