"""Networking for game clients

Functionality for communicating with the server for clients.
"""

import socket

from config import SERVER_ADDRESS, SERVER_PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        print("connecting to server...")

        self.client.connect((SERVER_ADDRESS, SERVER_PORT))
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
