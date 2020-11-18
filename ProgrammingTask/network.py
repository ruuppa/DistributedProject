"""Networking for game clients

Functionality for creating socket connections for clients.
"""

import socket
import pickle
from config import SERVER_ADDRESS, SERVER_PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.11.250.207"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    #def create_connection(self):
    #    print("connecting to server...")

    #    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    client.connect((SERVER_ADDRESS, SERVER_PORT))
    #    return client

    def getP(self):
        return self.getP

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.send(str.encode(data))
            return pickle.loads(client.recv(2048*2))
        except socket.error as e:
            print(e)