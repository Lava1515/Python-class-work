import socket

s = socket.socket()
s.bind(("127.0.0.3", 2000))
s.listen(10)

s_list = []
c_s, _ = s.accept()
while True:
    s_list.append(c_s)
    data = c_s.recv(2)
    print(data.decode())
    c_s, _ = s.accept()

