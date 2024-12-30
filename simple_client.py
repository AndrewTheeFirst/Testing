from Network import BaseClient
from Network.consts import *

class Client(BaseClient):
    def process(self, message: str):
        if message == IN:
            actual_message = self.server.crecv()
            print(actual_message)
            response = input()
            self.server.csend(response)
        elif message == CLEAR:
            actual_message = self.server.crecv()
            print(actual_message)
        else:
            print(message)

    def connect(self):
        try:
            self.server_addr = ("192.168.1.184", 5555)
            super().connect()
            if self.connected:
                print("success")
        except Exception as e:
                print(f"failure: {e}")
        else:
            if not self.connected:
                print("failed")

c = Client()
c.connect()
input("press Enter.")