import socket

Server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server_socket.bind(("0.0.0.0", 8821))
(data, remote_address) = Server_socket.recvfrom(1024)
print('The client sent: ' + data.decode())
Server_socket.sendto(data, remote_address)
Server_socket.close()




