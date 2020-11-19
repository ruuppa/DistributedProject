"""Networking for game clients

Functionality for creating socket connections for clients.
"""
"""test"""

import socket

#from config import SERVER_ADDRESS, SERVER_PORT
#server = "localhost"
#port = 5555


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost" # local ip
        self.port = 5555 
        self.addr = (self.server, self.port) #address
        self.id = self.create_connection() #player id, this is needes when there is multiple players
        print(self.id) # when connected this print id



    def create_connection(self):
        try:
            self.client.connect(self.addr) #connect to the server
            return self.client.recv(2040).decode() # encoded 
        except:
             pass


    def send(self, data): #send information to the server and back
        
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode # this returns the message from client
        except socket.error as error_message: #
            print(error_message)


n = Network()
print(n.send("hello"))

        
     #   print("connecting to server...")

 #       client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #       client.connect((server, port))
 #       return client


