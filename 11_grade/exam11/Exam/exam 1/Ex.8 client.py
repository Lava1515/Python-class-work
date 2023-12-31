import socket

s_list = []
for i in range(10):
    s = socket.socket()
    s_list.append(s)
    s.connect(("127.0.0.3", 2000))
    data = s.recv(1024)
    print(data.encode())