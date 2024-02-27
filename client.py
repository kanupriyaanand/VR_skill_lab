import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server's address and port
host = '127.0.0.1'
port = 12345
client_socket.connect((host, port))

# Receive and print messages from the server
while True:
    data_received = client_socket.recv(1024).decode()
    if not data_received:
        break

    print("Received from server:", data_received)

# Close the connection
client_socket.close()
