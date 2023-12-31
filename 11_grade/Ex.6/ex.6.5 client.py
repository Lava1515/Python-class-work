import socket
import time

My_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
time1 = time.time()
My_socket.sendto('Omer'.encode(), ('127.0.0.1', 8821))
(data, remote_address) = My_socket.recvfrom(1024)
time2 = time.time()
print('The server sent: ' + data.decode())
print('Time ' + str(time2 - time1))
My_socket.close()
