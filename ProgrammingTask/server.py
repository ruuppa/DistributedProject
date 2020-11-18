import socket
import pickle
from _thread import *
import sys
from game import Game

from config import SERVER_PORT, SERVER_ADDRESS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER_ADDRESS, SERVER_PORT))
except socket.error as e:
    print("socket error", str(e))

s.listen(3) #3 clients can connect
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, addr, gameId):
    global idCount
    conn.send(str.encode("Connected"))
    reply = ""

    while True:
        try:
            data = conn.recv(2048)

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except ConnectionResetError:
            # This happens when client cuts the connection.
            print(f"{addr}: connection reset")
            break

        reply = data.decode("utf-8")

        if not data:
            break
        else:
            print(f"Received from {addr}:", reply)

        conn.sendall(pickle.dumps(game))

    print(f"Client {addr} disconnected, terminating connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))

