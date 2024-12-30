from driver import Driver
from Network import Server
from Network.utils import LOG_PATH
from cursestools import Page, wread, center
import cursestools.consts as c
from time import sleep

IP = "192.168.1.184"
PORT = 5555

class Lobby(Server):
    pass

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
        binds = {'w': c.Dir.DOWN, 'a': c.Dir.RIGHT, 's': c.Dir.UP, 'd': c.Dir.LEFT}
        key = dri.stdscr.getkey()
        if key == c.ESC:
            log.cls()
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

def open_server(server: Server, screen: Driver):
    server.open()
    prompt(screen, "Opening Server")

def close_server(server: Server, screen: Driver):
    server.close()
    prompt(screen, "Closing Server")

def shutdown_server(server: Server, screen: Driver):
    server.shutdown()
    prompt(screen, "Shutting Down Server")

def setup_driver(server: Server):
    screen = Driver(f"IP: {IP} | PORT: {PORT}",
                     ["INIT / OPEN SERVER", "CLOSE SERVER", "SHUTDOWN SERVER", "VIEW LOG"])
    screen.add_onpress(0, lambda: open_server(server, screen))
    screen.add_onpress(1, lambda: close_server(server, screen))
    screen.add_onpress(2, lambda: shutdown_server(server, screen))
    screen.add_onpress(3, lambda: open_log(screen))
    return screen

if __name__ == "__main__":
    input("Press Enter to continue.")
    lobby = Lobby((IP, PORT), 5)
    screen = setup_driver(lobby)
    screen.event_loop()