from cursestools import *
import cursestools as c
import curses
from typing import Callable

BUTTON_HEIGHT = 3
BUTTON_WIDTH = 22

class Driver:
    def __init__(self, title: str = "", buttons: list[str] = None):
        self.stdscr = curses.initscr()
        self.stdscr.noutrefresh() # will prevent unwanted refreshes later
        curses.noecho() # typed keys will not be displayed on the window
        curses.cbreak() # program will not wait for the enter key to be pressed to react to input
        curses.curs_set(0) # make cursor invisible
        if curses.has_colors:
            curses.start_color()
            self.init_colors()
        self.running = True
        self.buttons = buttons if buttons else []
        self.on_press = {}
        self.title = title
        self.build()

        self.stdscr.keypad(True) # allows listening for arrow keys 

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    def build(self):
        '''places windows and refreshes the terminal'''
        self.header = self.make_header()
        self.main_screen = Panel(curses.LINES - 6, curses.COLS, 1, 0, outline=True)
        self.prompt_box = Panel(1, curses.COLS - 2, curses.LINES - 5, 1)
        self.text_box = TextBox(3, curses.COLS // 2, curses.LINES - 4, curses.COLS // 4)
        self.options = self.make_options()
        if self.buttons:
            self.setup_buttons()
        self.refresh_all()
        self.options.hide()
        curses.doupdate()
    
    def add_onpress(self, button: int, lmbda: Callable):
        self.on_press[button] = lmbda
    
    def refresh_all(self):
        self.header.noutrefresh()
        self.main_screen.noutrefresh()
        self.prompt_box.noutrefresh()
        self.text_box.noutrefresh()
        self.options.noutrefresh()

    def make_header(self):
        '''shows game title and any extra information'''
        header = curses.newwin(1, curses.COLS, 0, 0)
        offset_x = (curses.COLS - len(self.title)) // 2
        header.addstr(0, offset_x, self.title)
        return header

    def make_options(self):
        '''shows controls and any extra information'''
        footer = Panel(1, curses.COLS, curses.LINES - 1, 0)
        text = "| Press Q to Quit | Press R to Return to Main Menu | Press C to Chat |"
        offset_x = (curses.COLS - len(text)) // 2
        footer.addstr(0, offset_x, text)
        for label in ["Quit", "Return", "Chat"]:
            footer.chgat(0, offset_x + text.find(label) - 5, 1, curses.color_pair(1))
        return footer

    def setup_buttons(self):
        num_buttons = len(self.buttons)
        max_y, max_x = self.main_screen.getmaxyx()
        offset_x = (max_x - BUTTON_WIDTH) // 2
        offset_y = (max_y - BUTTON_HEIGHT * num_buttons + num_buttons - 1) // 2 - 1
        draw_button(offset_y, offset_x, BUTTON_HEIGHT, BUTTON_WIDTH, self.main_screen, self.buttons[0])

        self.pointer_start = (offset_y + 1, offset_x - 2)
        self.pointer_y = self.pointer_start[0]
        self.main_screen.addch(*self.pointer_start, '>')

        for index in range(1, num_buttons):
            offset_y = (max_y - BUTTON_HEIGHT * num_buttons + num_buttons - 1) // 2 - 1 + (index * BUTTON_HEIGHT)
            draw_button(offset_y, offset_x, BUTTON_HEIGHT, BUTTON_WIDTH, self.main_screen, self.buttons[index])

    def move_pointer(self, dir: Dir):
        self.main_screen.addch(self.pointer_y, self.pointer_start[1], ' ')
        highest = self.pointer_start[0]
        lowest = highest + BUTTON_HEIGHT * (len(self.buttons) - 1)
        if dir is Dir.UP:
            self.pointer_y = self.pointer_y - BUTTON_HEIGHT if highest < self.pointer_y else lowest
        elif dir is Dir.DOWN:
            self.pointer_y = self.pointer_y + BUTTON_HEIGHT if self.pointer_y < lowest else highest
        self.main_screen.addch(self.pointer_y, self.pointer_start[1], '>')
        self.main_screen.refresh()
    
    def get_pointed(self):
        return (self.pointer_y - self.pointer_start[0] ) // BUTTON_HEIGHT

    def close(self):
        self.running = False
        self.stdscr.keypad(0)
        curses.echo() # reverses curses.noecho()
        curses.nocbreak() # reverses curses.cbreak()
        curses.endwin() # restores default terminal
        raise SystemExit

    def event_loop(self):
        while self.running:
            key = self.stdscr.getkey()
            if key == ESC:
                self.options.toggle()
                if self.options.visible:
                    self.main_screen.hide()
                    self.prompt_box.hide()
                else:
                    self.main_screen.show()
                    self.prompt_box.show()
            elif self.options.visible:
                self.options_handler(key)
            elif self.main_screen.visible:
                self.menu_handler(key)
            else:
                self.text_box.proc_key(key)

    def menu_handler(self, key: str):
        match (key):
            case "KEY_UP" | ('w'):
                self.move_pointer(Dir.UP)
            case "KEY_DOWN" | 's':
                self.move_pointer(Dir.DOWN)
            case c.ENTER | ' ':
                self.on_press.get(self.get_pointed(), self.NOT_IMPLEMENTED)()

    def options_handler(self, key: str):
        match(key.upper()):
            case 'Q':
                self.close()
            case 'R':
                self.options.hide()
                self.main_screen.show()
                self.prompt_box.show()
            case 'C':
                self.options.hide()
                self.prompt_box.show()
    
    def NOT_IMPLEMENTED(self):
        self.close()
        raise Exception("Unimplemented Error")
    
if __name__ == "__main__":
    import signal

    def random_text(window: Panel):
        pad = curses.newpad(50, 50)
        for _ in range(50):
            pad.addstr("BANANASSS")
        window.set_overlay(pad)
    # signal.signal(signal.SIGWINCH, )
    d = Driver("Phase Ten", ["ADD OVERLAY", "REMOVE OVERLAY", "QUIT"])
    d.add_onpress(0, lambda: random_text(d.main_screen))
    d.add_onpress(1, lambda: d.main_screen.remove_overlay())
    d.event_loop()
