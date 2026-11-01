import socket
import threading

# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using its IP address and port
client.connect(('127.0.0.1', 5555))

# Ask the user to choose a nickname
nickname = input("Choose a nickname: ")


def receive():
    # Continuously listen for incoming messages from the server
    while True:
        try:
            # Receive data from the server and decode it
            message = client.recv(1024).decode('ascii')

            # Check if the server is requesting the client's nickname
            if message == 'NICK':
                # Send the nickname to the server
                client.send(nickname.encode('ascii'))
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
    # Continuously allow the user to send messages
    while True:
        # Format the message with the client's nickname
        message = f'{nickname}: {input("")}'

        # Encode and send the message to the server
        client.send(message.encode('ascii'))


# Create a separate thread to receive messages
receive_thread = threading.Thread(target=receive)

# Start the receiving thread
receive_thread.start()

# Create a separate thread to send messages
write_thread = threading.Thread(target=write)

# Start the writing thread
write_thread.start()