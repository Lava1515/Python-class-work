import socket

s = socket.socket()

for i in range(10):
    s.connect(("127.0.0.%s" % str(i), 2000))
    s.send(str(i).encode())
print("client connected")