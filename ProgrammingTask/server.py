import socket
from _thread import *
import sys

#from config import SERVER_PORT, SERVER_ADDRESS
server = "localhost"
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print("socket error", str(e))

s.listen(3) #3 clients can connect
print("Waiting for a connection, Server Started")

def threaded_client(conn, addr):
    conn.send(str.encode("Connected"))
    reply = ""

    while True:
        try:
            data = conn.recv(2048)
        except ConnectionResetError:
            # This happens when client cuts the connection.
            print(f"{addr}: connection reset")
            break

        reply = data.decode("utf-8")

        if not data:
            break
        else:
            print(f"Received from {addr}:", reply)

        conn.sendall(str.encode(reply))

    print(f"Client {addr} disconnected, terminating connection")
    conn.close()

while True:
    #print("test")
    conn, addr = s.accept()
    print("Connected to ", addr)
    start_new_thread(threaded_client, (conn, addr))
