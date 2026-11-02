
import socket
import threading

# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using its IP address and port number
client.connect(('127.0.0.1', 5555))

# Variable used to stop the client threads when necessary
stop_thread = False

# Ask the user to choose a nickname
nickname = input("Choose a nickname: ")

# Ask for the admin password if the chosen nickname is 'admin'
if nickname == 'admin':
    password = input("Enter password for admin: ")


def receive():
    # Continuously listen for incoming messages from the server
    while True:
        global stop_thread

        # Stop the receiving thread if requested
        if stop_thread:
            break

        try:
            # Receive data from the server and decode it
            message = client.recv(1024).decode('ascii')

            # Check if the server is requesting the client's nickname
            if message == 'NICK':

                # Send the chosen nickname to the server
                client.send(nickname.encode('ascii'))

                # Wait for the server's next response
                next_message = client.recv(1024).decode('ascii')

                # Check if the server is requesting the admin password
                if next_message == 'PASS':

                    # Send the admin password to the server
                    client.send(password.encode('ascii'))

                    # Check if the server refuses the connection
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password")
                        stop_thread = True

                # Check if the nickname is present in the ban list
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')

                    # Close the connection to the server
                    client.close()

                    # Stop the client threads
                    stop_thread = True

            else:
                # Display the received message in the console
                print(message)

        except:
            # Handle any error that occurs during message reception
            print("An error occurred!")

            # Close the client connection
            client.close()
            break


def write():
    # Continuously allow the user to send messages to the server
    while True:

        # Stop the writing thread if requested
        if stop_thread:
            break

        # Format the message by adding the client's nickname
        message = f'{nickname}: {input("")}'

        # Check if the message starts with a command
        if message[len(nickname) + 2:].startswith('/'):

            # Only the admin is allowed to execute commands
            if nickname == 'admin':

                # Check if the admin wants to kick a user
                if message[len(nickname) + 2:].startswith('/kick'):

                    # Send the KICK command and the target user's nickname
                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))

                # Check if the admin wants to ban a user
                elif message[len(nickname) + 2:].startswith('/ban'):

                    # Send the BAN command and the target user's nickname
                    client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))

            else:
                # Inform non-admin users that commands are restricted
                print("Commands can only be executed by the admin!")

        else:
            # Encode and send the message to the server
            client.send(message.encode('ascii'))


# Create a separate thread to receive messages from the server
receive_thread = threading.Thread(target=receive)

# Start the receiving thread
receive_thread.start()

# Create a separate thread to send messages to the server
write_thread = threading.Thread(target=write)

# Start the writing thread
write_thread.start()
