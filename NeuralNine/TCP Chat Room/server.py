import threading
import socket

# Define the server's IP address (localhost) and port
host = '127.0.0.1' # localhost
port = 5555

# Create a TCP socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified host and port
server.bind((host, port))

# Start listening for incoming client connections
server.listen()

# Store all connected clients
clients = []

# Store the nicknames of connected clients
nicknames = []


def broadcast(message):
    # Send a message to all connected clients
    for client in clients:
        client.send(message)


def handle(client):
    # Handle incoming messages from a specific client
    while True:
        try:
            # Receive a message from the client
            message = client.recv(1024)

            # Forward the received message to all connected clients
            broadcast(message)

        except:
            # Find the client's position in the clients list
            index = clients.index(client)

            # Remove the disconnected client from the list
            clients.remove(client)

            # Close the client's connection
            client.close()

            # Retrieve the nickname of the disconnected client
            nickname = nicknames[index]

            # Notify all remaining clients that the user has left
            broadcast(f"{nickname} left the chat".encode('ascii'))

            # Remove the nickname from the list
            nicknames.remove(nickname)
            break


def receive():
    # Continuously accept new client connections
    while True:
        # Accept an incoming connection
        client, address = server.accept()

        # Display the address of the newly connected client
        print(f"Connected with {str(address)}")

        # Request the client's nickname
        client.send("NICK".encode('ascii'))

        # Receive and decode the client's nickname
        nickname = client.recv(1024).decode('ascii')

        # Add the nickname and client to their respective lists
        nicknames.append(nickname)
        clients.append(client)

        # Display the nickname of the connected client
        print(f"Nickname of the client is {nickname}")

        # Notify all clients that a new user has joined
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        # Send a welcome message to the new client
        client.send('Connected to the server'.encode('ascii'))

        # Create a separate thread to handle this client
        thread = threading.Thread(target=handle, args=(client,))

        # Start the client handling thread
        thread.start()


# Display a message indicating that the server is running
print("Server is listening...")

# Start accepting incoming client connections
receive()