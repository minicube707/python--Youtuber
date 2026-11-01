import socket

# Create a UDP socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the server to localhost and port 9999
server.bind(('127.0.0.1', 9999))

# Receive a message from a client and retrieve its address
message, address = server.recvfrom(1024)

# Decode and display the received message
print(message.decode('utf-8'))

# Send a response back to the client using its address
server.sendto("Hello Client!".encode('utf-8'), address)