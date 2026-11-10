import socket
import threading

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")


def threaded_client(conn):

    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                print("Diconnected")
                break
            else:
                print("Recieved: ", reply)
                print("Sending: ", reply)

            conn.sendall(reply.encode('utf-8'))
        
        except:
            break


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread = threading.Thread(target=threaded_client, args=(conn, )).start()