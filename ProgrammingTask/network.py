"""Networking for game clients

Functionality for creating socket connections for clients.
"""

import socket
import pickle
from config import SERVER_ADDRESS, SERVER_PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_ADDRESS
        self.port = SERVER_PORT
        self.addr = (self.server, self.port)
        self.playerId = self.connect()

    def getPlayerId(self):
        return self.playerId

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except InterruptedError as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except (OSError, pickle.UnpicklingError) as e:
            print(e)
