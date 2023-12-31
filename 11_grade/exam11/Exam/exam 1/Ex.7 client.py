import socket

s_list = []
for i in range(10):
    s = socket.socket()
    s_list.append(s)
    s.connect(("127.0.0.3", 2000))
    print("client connected")

i = 0
for s in s_list:
    i = i + 1
    s.send(str(i).encode())
