import socket
import pickle
from _thread import start_new_thread
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

def threaded_client(conn, playerId, gameId):
    global idCount
    conn.send(str.encode(str(playerId)))

    while True:
        try:
            data = conn.recv(2048*2).decode('utf-8')

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        print("Got a play:", playerId, data)
                        game.play(playerId, data)

                    conn.sendall(pickle.dumps(game))
            else:
                print("Invalid game id", gameId, ", list of games:", games)
                break
        except ConnectionResetError:
            # This happens when client cuts the connection.
            print(f"{playerId}: connection reset")
            break

        if not data:
            print("Got no data!")
            break
        else:
            #print(f"Received from {playerId}:", data)
            pass

        conn.sendall(pickle.dumps(game))

    print(f"Client {playerId} disconnected, terminating connection")
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
    gameId = (idCount - 1)//3
    if idCount % 3 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    elif idCount % 3 == 2:
        print("Player 2 connected")
        p = 1
    elif idCount % 3 == 0:
        print("Player 3 connected, starting game")
        games[gameId].ready = True
        p = 2

    start_new_thread(threaded_client, (conn, p, gameId))

