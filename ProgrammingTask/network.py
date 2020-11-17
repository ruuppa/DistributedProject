"""Networking for game clients

Functionality for creating socket connections for clients.
"""

import socket

from config import SERVER_ADDRESS, SERVER_PORT


class Network:
    def create_connection(self):
        print("connecting to server...")

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDRESS, SERVER_PORT))
        return client
