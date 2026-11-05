import socket
import tqdm
from Crypto.Cipher import AES

# Define the AES encryption key and nonce
# Both must be 16 bytes long for AES
key = b"TheNeuralNineKey"
nonce = b"TheNeuralNineNce"

# Create an AES cipher using EAX mode
cipher = AES.new(key, AES.MODE_EAX, nonce)


# Create a TCP socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to localhost on port 9999
server.bind(("localhost", 9999))

# Start listening for incoming connections
server.listen()


# Accept an incoming connection from a client
client, addr = server.accept()


# Receive the file name from the client and decode it
file_name = client.recv(1024).decode()

# Receive the file size from the client and decode it
file_size = client.recv(1024).decode()


# Display the received file information
print(f"\nFile name: {file_name}")
print(f"File size: {file_size}")


# Open a new file in binary write mode
file = open(file_name, "wb")

# Initialize an empty byte string to store the received data
file_bytes = b""

# Initialize the transfer completion flag
done = False


# Create a progress bar to track the file transfer
# Display the progress in bytes with automatic unit scaling
progress = tqdm.tqdm(
    unit="B",
    unit_scale=True,
    unit_divisor=1_000,
    total=int(file_size)
)


# Continue receiving data until the transfer is marked as complete
while not done:

    # Receive up to 1024 bytes from the client
    data = client.recv(1024)

    # Check if the received data contains the end marker
    if file_bytes[-5:] == b"<END>":
        done = True
    else:
        # Add the received data to the file buffer
        file_bytes += data

    # Update the progress bar with the received data
    progress.update(len(data))


# Remove the end marker and decrypt the received file data
# Write the decrypted content into the output file
file.write(cipher.decrypt(file_bytes[:-5]))


# Close the file after writing the decrypted data
file.close()

# Close the client connection
client.close()

# Close the server socket
server.close()


# Display a message indicating that the transfer is finished
print("\nTransfer finished!")