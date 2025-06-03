import socket

host = "192.168.1.38"
port = 9999

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((host, port))
print("Serveur is open")
serveur.listen(5)


while True:
    communication_socket, adress  = serveur.accept()
    print(f"Connected to {adress}")
    
    message = communication_socket.recv(1024).decode("utf-8")
    print(f"Message from client is: {message}")

    communication_socket.send("Message recived".encode())
    communication_socket.close()

    print(f"Connection close with {adress}")