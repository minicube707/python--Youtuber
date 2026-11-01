import socket

# Create a TCP socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to localhost and port 9999
server.bind(('127.0.0.1', 9999))

# Start listening for incoming client connections
server.listen()


# Continuously accept incoming client connections
while True:
    # Accept a new client connection
    client, address = server.accept()

    # Display the address of the connected client
    print(f"Connected to {address}")

    # Receive a message from the client and decode it
    print(client.recv(1024).decode("utf-8"))

    # Send a greeting message to the client
    client.send("Hello Client!".encode('utf-8'))

    # Receive another message from the client and decode it
    print(client.recv(1024).decode("utf-8"))

    # Send a goodbye message to the client
    client.send("Bye!".encode('utf-8'))

    # Close the client's connection
    client.close()