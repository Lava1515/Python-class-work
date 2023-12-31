import socket
import os

my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 80))
my_socket.send(b"GET /index.html HTTP/1.1")
data =""

while "\r\n\r\n" not in data:
    data += my_socket.recv(1).decode()
data =data.split("\r\n")[1]
leangth =int(data.split()[-1])
data = my_socket.recv(leangth)
print(data)
data = data[82:]
with open(r'save_index.html', "wb") as file:
    file.write(data)
os.startfile("save_index.html")

print(data)





