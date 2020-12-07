"""Networking for game clients

Functionality for creating socket connections for clients.
"""

import socket
import pickle
import logging
from datetime import datetime

from config import SERVER_ADDRESS, SERVER_PORT

logger = logging.getLogger(__name__)


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_ADDRESS
        self.port = SERVER_PORT
        self.addr = (self.server, self.port)
        self.playerId = self.connect()
        self.lastPingTime = datetime.utcnow()

    def getPlayerId(self):
        return self.playerId

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except InterruptedError:
            logger.exception('error connecting the client')

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except (OSError, pickle.UnpicklingError):
            logger.exception('error sending data')

    def ping(self):
        timePassed = datetime.utcnow() - self.lastPingTime
        if timePassed.microseconds >= 500000: # Pings every 0.5 seconds
            self.lastPingTime = datetime.utcnow()
            self.send('get')
            ping = datetime.utcnow() - self.lastPingTime
            return ping.microseconds // 1000 # Returns milliseconds
        return None
