from Network import BaseClient
from Network.consts import *
from driver import Driver
from cursestools import Dir, Page, wread, center
import cursestools.consts as c
from Network.utils import add_to_log, LOG_PATH
from time import sleep

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

def setup_log(dri: Driver):
    with open(LOG_PATH, 'r') as log:
        lines = log.readlines()
    width = max([len(line) for line in lines]) + 1
    height = len(lines) * 2 + 1
    p = Page(dri.main_screen, height=height, width=width)
    p.out("\n".join(lines), end="")
    return p

def open_log(dri: Driver):
    log = setup_log(dri)
    while True:
        binds = {'w': Dir.DOWN, 'a': Dir.RIGHT, 's': Dir.UP, 'd': Dir.LEFT}
        key = dri.stdscr.getkey()
        if key == c.ESC:
            break
        elif key in binds:
            log.shift(binds[key], 2)
            log.refresh()
    dri.main_screen.show()

def prompt(screen: Driver, text: str):
    wread(screen.prompt_box, 
          0, center(screen.prompt_box, text)[1],
            text)
    screen.prompt_box.clear()
    screen.prompt_box.noutrefresh()
    sleep(1)

def connect(screen: Driver, client: Client):
    try:
        client.server_addr = ("192.168.1.184", 5555)
        client.connect()
        if client.connected:
            print("success")
    except Exception as e:
            print(f"failure: {e}")
    screen.close()
    

if __name__ == "__main__":
    input("Press Enter to continue.")
    client = Client()
    screen = Driver("Client", ["Connect to Server", "Disconnect", "View Log"])
    screen.add_onpress(0, lambda: connect(screen, client))
    screen.add_onpress(1, lambda: add_to_log("Disconnect..."))
    screen.add_onpress(2, lambda: open_log(screen))
    screen.event_loop()


# def connect(screen: Driver, client: Client):
#     from threading import Thread
#     def f():
#         screen.main_screen.hide()
#         prompt(screen, "IP:")
#         ip = screen.text_box.get_text()
#         prompt(screen, "PORT:")
#         port = screen.text_box.get_text()
#         if port.isnumeric():
#             client.server_addr = (ip, int(port))
#             client.connect()
#         if client.connected:
#             prompt(screen, "Connection Successful.")
#         else:
#             prompt(screen, "Failed to Connect.")
#     Thread(target=f).start()