from protocol import Protocol

# Create and connect the client
client_protocol = Protocol()
client_protocol.connect(('localhost', 12345))

# Sending a message
client_protocol.send_msg("Hello, Server!")

# Receiving a message
try:
    msg = client_protocol.get_msg()
    print(f"Received: {msg}")
except Exception as e:
    print(f"Error receiving message: {e}")

client_protocol.close()
