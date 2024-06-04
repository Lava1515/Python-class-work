from protocol import Protocol
from generate_cert_and_key import check_and_generate_cert_and_key

# Paths to certificate and key files
certfile = 'certfile.pem'
keyfile = 'keyfile.pem'

# Ensure certificate and key files exist
check_and_generate_cert_and_key(certfile, keyfile)

# Create and start the server
server_protocol = Protocol(is_server=True, certfile=certfile, keyfile=keyfile)
server_protocol.bind(('localhost', 12345))
server_protocol.listen()
print("Server listening on port 12345...")

while True:
    client_protocol, addr = server_protocol.accept()
    print(f"Accepted connection from {addr}")

    # Receiving a message
    # try:
    msg = client_protocol.get_msg()
    print(f"Received: {msg.decode()}")
    # except Exception as e:
    # print(f"Error receiving message: {e}")

    # Sending a message
    # try:
    client_protocol.send_msg("fafafafafaf, Client!")
    # except Exception as e:
    #     print(f"Error sending message: {e}")

    client_protocol.close()
