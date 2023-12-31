import socket
import time

s = socket.socket()
s.bind(("127.0.0.2", 2000))
s.listen()
print("a")
s_list = []
c_s, _ = s.accept()
print(_)
while True:
    print("a")
    s_list.append(c_s)
    data = c_s.recv(100)
    print(data.decode())
    c_s, _ = s.accept()
    print("client accepted in server")