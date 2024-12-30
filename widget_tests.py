import curses
from curses import window
from cursestools import Panel, TextBox, FreeWindow, Dir
from time import sleep
from random import randrange
from cursestools.utils import Key

def panel_test(stdscr: window):
    panel1 = Panel(5, 30, 5, 5, outline=True)
    panel1.addstr("Panel1 Content")
    panel1.noutrefresh()
                  
    panel2 = Panel(5, 30, 7, 6, outline=True)
    panel2.addstr("\n\nPanel2 Content")
    panel2.noutrefresh()

    curses.doupdate()
    stdscr.getch()

    for panel in [panel1, panel2]:
        panel.hide()
        curses.doupdate()
        stdscr.getch()
    for panel in [panel1, panel2]:
        panel.show()
        curses.doupdate()
        stdscr.getch()

def textbox_test(stdscr: window):
    tb = TextBox(10, 100, 10, 10)
    for letter in "Bananas in Paris ":
        sleep(0.1)
        tb.proc_key(letter)
    stdscr.getch()
    for letter in ". . . ":
        sleep(0.5)
        tb.proc_key(letter)
    stdscr.getch()
    for letter in "BOOOO!":
        tb.proc_key(letter)
    stdscr.getch()

def console_test(stdscr: window):

    ### FILLING CONTENT
    mycons = FreeWindow(stdscr)
    max_y, max_x = mycons.getmaxyx()
    for y in range(max_y - 1):
        for x in range(max_x - 1):
            num = randrange(32, 126)
            char = chr(num)
            mycons.addch(y, x, char)
    mycons.refresh()
    stdscr.getch()

    ### BOUNDARY BEHAVIOR
    for _ in range(max_y - 1):
        sleep(0.005)
        mycons.shift(Dir.UP)
        mycons.refresh()
    stdscr.getch()
    mycons.shift(Dir.DOWN)
    mycons.refresh()
    stdscr.getch()

    mycons.reset_offset()
    mycons.refresh()
    stdscr.getch()

    ### STANDARD SCROLLING
    for _ in range(2):
        for _ in range(2):
            mycons.shift(Dir.UP)
            mycons.refresh()
            stdscr.getch()
        for _ in range(2):
            mycons.shift(Dir.DOWN)
            mycons.refresh()
            stdscr.getch()
    for _ in range(2):
        for _ in range(2):
            mycons.shift(Dir.LEFT)
            mycons.refresh()
            stdscr.getch()
        for _ in range(2):
            mycons.shift(Dir.RIGHT)
            mycons.refresh()
            stdscr.getch()

def main(stdscr: window):
    curses.curs_set(2)
    stdscr.box()
    stdscr.noutrefresh()
    curses.doupdate()
    stdscr.keypad(1)
    key = Key(stdscr.getch())
    match (key):
        case 'w' | curses.KEY_UP:
            print("yes")
        case _:
            print("no")
    # panel_test(stdscr)
    # textbox_test(stdscr)
    # console_test(stdscr)

curses.wrapper(main)