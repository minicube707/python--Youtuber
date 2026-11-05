import os
import socket


# Create a TCP socket to establish a connection with the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server running on localhost, port 9999
client.connect(('localhost', 9999))

# Ask the user to enter the path of the file to transfer
# Remove any quotation marks surrounding the path
path_to_file = input("Enter the path to the file: ").strip('"')

# Check if the specified file exists
if not os.path.isfile(path_to_file):
    print("File not found!")
    exit()

# Extract the file name from the complete file path
filename = os.path.basename(path_to_file)

# Get the size of the file in bytes
file_size = os.path.getsize(path_to_file)

# Display information about the file
print(f"\nPath to file: {path_to_file}")
print(f"File: {filename}")
print(f"File size: {file_size} bytes")

# Open the file in binary read mode
file = open(path_to_file, "rb")

# Get the file size again
file_size = os.path.getsize(path_to_file)

# Send the file name to the server with the "received_" prefix
client.send(f"received_{filename}".encode())

# Send the file size to the server as a string
client.send(str(file_size).encode())

# Read the entire file content
data = file.read()

# Send all the file data to the server
client.sendall(data)

# Send an end marker to indicate that the transfer is finished
client.send(b"<END>")


# Close the file after reading its contents
file.close()

# Close the socket connection
client.close()

# Display a confirmation message
print("\nTransfer finished!")