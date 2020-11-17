import socket
from _thread import *
import sys

from config import SERVER_PORT, SERVER_ADDRESS


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER_ADDRESS, SERVER_PORT))
except socket.error as e:
    str(e)

s.listen(3) #3 clients can connect
print("Waiting for a connection, Server Started")

def threaded_client(conn, addr):
    conn.send(str.encode("Connected"))
    reply = ""

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print(f"Received from {addr}:", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to ", addr)
    start_new_thread(threaded_client, (conn, addr))
