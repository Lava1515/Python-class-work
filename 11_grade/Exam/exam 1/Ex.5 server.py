import socket
import time

s = socket.socket()
s.bind(("127.0.0.5", 2000))
s.listen()
s.settimeout(2)
while True:
    try:
        (clint_s, client_ip) = s.accept()
    except socket.timeout:
        break
    data = clint_s.recv(1)
    print(data.decode())
    print("client accepted in server")