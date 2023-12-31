import socket
import time

s = socket.socket()
s.bind(("127.0.0.3", 2000))
s.listen(2)

s_list = []
c_s, _ = s.accept()
while True:
    s_list.append(c_s)
    c_s.send(f"connected so {len(s_list)} connected".decode())
    c_s, _ = s.accept()

print("client accepted in server")