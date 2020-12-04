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

class RPSServer:
    def __init__(self):
        self.games = {}
        self.idCount = 0

    def player_client(self, conn, playerId, gameId):
        conn.send(str.encode(str(playerId)))

        while True:
            try:
                raw_bytes = conn.recv(2048*2)

                try:
                    data = raw_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    logger.exception(f'received undecodable bytes: {raw_bytes}')
                    continue

                if gameId in self.games:
                    game = self.games[gameId]

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
                    logger.info(f"{gameId} is missing, exiting game...")
                    break
            except ConnectionResetError:
                # This happens when client cuts the connection.
                logger.warning(f"{playerId}: connection reset")
                break
            except InterruptedError as e:
                logger.warning(e)
                break

        logger.info(f"Client {playerId} disconnected, terminating connection")

        if gameId in self.games:
            del self.games[gameId]
            logger.info(f'deleted game {gameId}')
        else:
            logger.info(f"didn't terminate game {gameId} because it was already deleted")

        self.idCount -= 1
        conn.close()

    def run(self):
        logger.info("Waiting for a connection, Server Started")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # See https://stackoverflow.com/a/6380198
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Hardcode 0.0.0.0 as address, since we should be using that for all
        # use cases.
        s.bind(("0.0.0.0", SERVER_PORT))

        s.listen(3)  # 3 clients can connect

        while True:
            conn, addr = s.accept()
            logger.info(f"Connected to: {addr}")

            self.idCount += 1
            p = 0
            gameId = (self.idCount - 1)//3
            if self.idCount % 3 == 1:
                self.games[gameId] = Game(gameId)
                logger.info("Creating a new game... Player 0 connected")
            elif self.idCount % 3 == 2:
                logger.info("Player 1 connected")
                p = 1
                self.games[gameId].playerJoined(1)
            elif self.idCount % 3 == 0:
                logger.info("Player 2 connected, starting game")
                self.games[gameId].ready = True
                p = 2
                self.games[gameId].playerJoined(2)

            start_new_thread(self.player_client, (conn, p, gameId))

if __name__ == '__main__':
    server = RPSServer()

    server.run()
