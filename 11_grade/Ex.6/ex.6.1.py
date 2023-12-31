import socket
import time

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))
time1 = time.time()
my_socket.send('liav'.encode())
print('I am connected')
data = my_socket.recv(1024)
time2 = time.time()
print("client recv " + data.decode())
print("time took " + str(time2 - time1))
