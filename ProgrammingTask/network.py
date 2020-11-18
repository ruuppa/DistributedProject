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

    #def create_connection(self):
    #    print("connecting to server...")

    #    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    client.connect((SERVER_ADDRESS, SERVER_PORT))
    #    return client

    def getPlayerId(self):
        return self.playerId

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            print("Sending:", data)
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
