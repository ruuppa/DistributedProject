import socket
import pickle
from _thread import start_new_thread
import sys
from datetime import datetime
import logging

from game import Game
from config import SERVER_PORT, SERVER_ADDRESS, LOG_LEVEL


logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER_ADDRESS, SERVER_PORT))
except OSError as e:
    logger.exception("socket error")

s.listen(3) #3 clients can connect
logger.info("Waiting for a connection, Server Started")

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
                    logger.warning("No data.")
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        logger.info(f"Got a play: {playerId} {data}")
                        benchmark_start = datetime.now()
                        game.play(playerId, data)

                        elapsed = datetime.now() - benchmark_start

                        logger.info(f'calculated next game state in {elapsed.microseconds} us')

                    conn.sendall(pickle.dumps(game))
            else:
                logger.warning("Invalid game id: {gameId}, list of games: {games}")
                break
        except ConnectionResetError:
            # This happens when client cuts the connection.
            logger.warning(f"{playerId}: connection reset")
            break
        except InterruptedError as e:
            logger.warning(e)
            break

    logger.info(f"Client {playerId} disconnected, terminating connection")
    try:
        del games[gameId]
        logger.info(f"Closing Game {gameId}")
    except NameError:
        logger.exception('error closing game')

    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    logger.info(f"Connected to: {addr}")

    idCount += 1
    p = 0
    gameId = (idCount - 1)//3
    if idCount % 3 == 1:
        games[gameId] = Game(gameId)
        logger.info("Creating a new game...")
    elif idCount % 3 == 2:
        logger.info("Player 2 connected")
        p = 1
    elif idCount % 3 == 0:
        logger.info("Player 3 connected, starting game")
        games[gameId].ready = True
        p = 2

    start_new_thread(threaded_client, (conn, p, gameId))
