from protocol import Protocol
import socket
import threading

# Function to handle client connections
def handle_client(client_protocol, address):
    print(f"[NEW CONNECTION] {address} connected.")

    # Echo loop
    while True:
        try:
            # Receive data from the client
            data = client_protocol.get_msg()
            if not data:
                print(f"[{address}] disconnected.")
                break

            print(f"[{address}] {data.decode('utf-8')}")

            # Echo the received data back to the client
            client_protocol.send_msg(data)
        except ConnectionError:
            print(f"[{address}] connection closed unexpectedly.")
            break

    # Close the connection
    client_protocol.close()

# Server configuration
HOST = '127.0.0.1'
PORT = 5555

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a Protocol instance
server_protocol = Protocol(server_socket)

# Bind the socket to the host and port
server_protocol.bind((HOST, PORT))

# Listen for incoming connections
server_protocol.listen()

print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

# Main loop to accept incoming connections
while True:
    # Accept a new connection
    client_protocol, address = server_protocol.accept()

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_protocol, address))
    client_thread.start()
