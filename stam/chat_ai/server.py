import socket
import threading
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 8080

# Data storage for chats
chats = {}


# Function to handle client connections
def handle_client(client_socket, username):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Decode the received data as JSON
            message = json.loads(data.decode('utf-8'))

            # Check the message type
            if message['type'] == 'message':
                # Get the recipient username
                recipient = message['recipient']

                # Get the recipient's socket
                recipient_socket = chats.get(recipient, None)

                # Send the message to the recipient
                if recipient_socket:
                    recipient_socket.send(data)
            elif message['type'] == 'join':
                # Add the client's socket to the chat list
                chats[username] = client_socket
        except Exception as e:
            print(f"Error handling client {username}: {e}")
            break


# Start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on http://{HOST}:{PORT}")

while True:
    # Accept incoming connections
    client_socket, addr = server.accept()

    # Receive the username from the client
    username = client_socket.recv(1024).decode('utf-8')

    # Create a thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
    client_handler.start()
