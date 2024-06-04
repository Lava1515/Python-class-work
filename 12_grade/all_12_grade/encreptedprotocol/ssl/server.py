from protocol import Protocol
import socket

def start_server():
    server_socket = Protocol(socket.socket(socket.AF_INET, socket.SOCK_STREAM), is_client=False)
    server_socket.bind(('localhost', 65432))
    server_socket.listen()
    print('Server is listening...')

    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')

    decrypted_message = conn.get_msg()
    print(f'Decrypted message from client: {decrypted_message.decode("utf-8")}')

    response_message = 'Message received'
    conn.send_msg(response_message.encode('utf-8'))

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
