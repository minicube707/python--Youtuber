import socket

host = "127.0.0.1"
port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

client.send("Hello world".encode("utf-8"))
print(client.recv(1024).decode())