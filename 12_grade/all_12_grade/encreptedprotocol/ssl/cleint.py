from protocol import Protocol
import socket

def start_client():
    client_socket = Protocol(socket.socket(socket.AF_INET, socket.SOCK_STREAM), is_client=True)
    client_socket.connect(('localhost', 65432))

    message = 'Hello, Server!'
    client_socket.send_msg(message.encode('utf-8'))

    decrypted_response = client_socket.get_msg()
    print(f'Decrypted response from server: {decrypted_response.decode("utf-8")}')

    client_socket.close()

if __name__ == "__main__":
    start_client()
