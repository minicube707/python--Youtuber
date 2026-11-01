import socket

# Create a UDP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a message to the server using its IP address and port
client.sendto('Hello Server!'.encode('utf-8'), ('127.0.0.1', 9999))

# Receive the server's response and decode it
print(client.recvfrom(1024)[0].decode('utf-8'))