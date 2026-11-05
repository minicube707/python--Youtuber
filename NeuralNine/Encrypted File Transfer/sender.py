import os
import socket
from Crypto.Cipher import AES

# Define the AES encryption key and nonce
# Both must be 16 bytes long for AES
key = b"TheNeuralNineKey"
nonce = b"TheNeuralNineNce"

# Create an AES cipher using EAX mode
cipher = AES.new(key, AES.MODE_EAX, nonce)


# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server running on localhost, port 9999
client.connect(("localhost", 9999))


# Ask the user to enter the path of the file to transfer
# Remove any quotation marks surrounding the path
path_to_file = input("Enter the path to the file: ").strip('"')


# Check if the specified file exists
if not os.path.isfile(path_to_file):
    print("File not found!")
    exit()


# Extract the file name from the complete file path
filename = os.path.basename(path_to_file)

# Get the size of the original file in bytes
file_size = os.path.getsize(path_to_file)


# Display information about the file
print(f"\nPath to file: {path_to_file}")
print(f"File: {filename}")
print(f"File size: {file_size} bytes")


# Open the file in binary read mode
with open(path_to_file, "rb") as f:

    # Read the entire file content
    data = f.read()


# Encrypt the file data using AES in EAX mode
encrypted = cipher.encrypt(data)


# Send the file name to the server with the "received_" prefix
client.send(f"received_{filename}".encode())

# Send the original file size to the server
client.send(str(file_size).encode())

# Send the encrypted file data to the server
client.sendall(encrypted)

# Send an end marker to indicate that the transfer is complete
client.send("<END>".encode())


# Close the client socket connection
client.close()