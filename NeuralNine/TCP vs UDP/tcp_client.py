import socket

# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using its IP address and port
client.connect(('127.0.0.1', 9999))

# Send a greeting message to the server
client.send("Hello Server".encode('utf-8'))

# Receive and display the server's response
print(client.recv(1024).decode('utf-8'))

# Send a goodbye message to the server
client.send("Bye".encode('utf-8'))

# Receive and display the server's final response
print(client.recv(1024).decode('utf-8'))