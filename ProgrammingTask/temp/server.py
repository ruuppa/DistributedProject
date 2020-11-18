import socket
from _thread import *
import pickle
from game import Game
from config import SERVER_ADDRESS, SERVER_PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER_ADDRESS, SERVER_PORT))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    print("No data.")
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                print("No gameId in games.")
                break
        except:
            print("Something went wrong here")
            break

    print("Lost connection")
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

    # We want to connect to all of the other clients, and no more.
    # Currently we crash if we try to do more than 3, but that is fine.
    idCount += 1
    p = 0
    gameId = (idCount - 1)//3 # We can use this to get extra games, currently set for 3 players each
    print("GameID: ",gameId)
    print("Idcount: ",idCount)

    ## There are smarter ways to make this, but with this, we can have infinite amount of 3 player games going at the same time
    if (idCount+2) % 3 == 0:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    elif (idCount+1) % 3 == 0:
        p = 1
    else:
        games[gameId].ready = True
        p = 2

    start_new_thread(threaded_client, (conn, p, gameId))