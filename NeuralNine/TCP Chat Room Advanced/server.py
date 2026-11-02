
import threading
import socket

# Define the server's IP address (localhost) and port number
host = '127.0.0.1'  # Localhost address
port = 5555  # Port used by the server

# Create a TCP socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified IP address and port
server.bind((host, port))

# Start listening for incoming client connections
server.listen()

# List used to store all connected clients
clients = []

# List used to store the nicknames of connected clients
nicknames = []


def broadcast(message):
    # Send the received message to every connected client
    for client in clients:
        client.send(message)


def handle(client):
    # Handle all incoming messages from a specific client
    while True:
        try:
            # Receive data sent by the client
            msg = message = client.recv(1024)

            # Check if the received message is a KICK command
            if msg.decode('ascii').startswith('KICK'):

                # Check whether the client sending the command is the admin
                if nicknames[clients.index(client)] == 'admin':
                    # Extract the nickname of the user to be kicked
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    # Refuse the command if the client is not an admin
                    client.send('Command was refused!'.encode('ascii'))

            # Check if the received message is a BAN command
            elif msg.decode('ascii').startswith('BAN'):

                # Check whether the client sending the command is the admin
                if nicknames[clients.index(client)] == 'admin':
                    # Extract the nickname of the user to be banned
                    name_to_ban = msg.decode('ascii')[4:]

                    # Kick the user from the server
                    kick_user(name_to_ban)

                    # Add the user's nickname to the ban list
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')

                    # Display a message confirming the ban
                    print(f'{name_to_ban} was banned!')
                else:
                    # Refuse the command if the client is not an admin
                    client.send('Command was refused!'.encode('ascii'))

            else:
                # Forward the message to all connected clients
                broadcast(message)

        except:

            # Check whether the client is still in the clients list
            if client in clients:

                # Find the client's position in the clients list
                index = clients.index(client)

                # Remove the disconnected client from the clients list
                clients.remove(client)

                # Close the client's socket connection
                client.close()

                # Retrieve the nickname of the disconnected client
                nickname = nicknames[index]

                # Notify all remaining clients that this user has left
                broadcast(f"{nickname} left the chat".encode('ascii'))

                # Remove the nickname from the nicknames list
                nicknames.remove(nickname)

                # Stop handling messages from this client
                break


def receive():
    # Continuously wait for new client connections
    while True:

        # Accept a new incoming client connection
        client, address = server.accept()

        # Display the address of the newly connected client
        print(f"Connected with {str(address)}")

        # Ask the client to provide a nickname
        client.send("NICK".encode('ascii'))

        # Receive and decode the client's nickname
        nickname = client.recv(1024).decode('ascii')

        # Read the list of banned nicknames from the file
        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        # Check whether the nickname is present in the ban list
        if nickname + '\n' in bans:
            # Inform the client that they are banned
            client.send('BAN'.encode('ascii'))

            # Close the connection and skip to the next client
            client.close()
            continue

        # Check whether the connecting client is the admin
        if nickname == 'admin':

            # Request the admin password
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            # Verify the admin password
            if password != 'adminpass':
                # Refuse the connection if the password is incorrect
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        # Add the new client and nickname to their respective lists
        nicknames.append(nickname)
        clients.append(client)

        # Display the nickname of the newly connected client
        print(f"Nickname of the client is {nickname}")

        # Notify all connected clients that a new user has joined
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        # Send a welcome message to the newly connected client
        client.send('Connected to the server'.encode('ascii'))

        # Create a new thread to handle this client's communication
        thread = threading.Thread(target=handle, args=(client,))

        # Start the thread so the server can handle multiple clients simultaneously
        thread.start()


def kick_user(name):
    # Check whether the requested nickname exists in the connected clients list
    if name in nicknames:

        # Find the position of the user in the nicknames list
        name_index = nicknames.index(name)

        # Retrieve the corresponding client socket
        client_to_kick = clients[name_index]

        # Remove the client from the connected clients list
        clients.remove(client_to_kick)

        # Notify the user that they have been kicked by an admin
        client_to_kick.send('You are kicked by an admin!'.encode('ascii'))

        # Close the user's socket connection
        client_to_kick.close()

        # Remove the user's nickname from the nicknames list
        nicknames.remove(name)

        # Notify all remaining clients that the user has been kicked
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))


# Display a message indicating that the server is running
print("Server is listening...")

# Start the server and begin accepting incoming connections
receive()
