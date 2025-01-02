import curses
from curses import window
from cursestools import Panel, Terminal, FreeWindow, TextBox, Dir, Align
from time import sleep
from random import randrange

def main(stdscr: window):
    curses.curs_set(2)
    stdscr.box()
    stdscr.noutrefresh()
    curses.doupdate()
    
    textbox_test(stdscr)
    panel_test(stdscr)
    terminal_test(stdscr)
    console_test(stdscr)

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

def terminal_test(stdscr: window):

    terminal = Terminal(10, 100, 10, 10)
    for letter in "Bananas in Paris ":
        sleep(0.1)
        terminal.proc_key(letter)
    stdscr.getch()
    for letter in ". . . ":
        sleep(0.1)
        terminal.proc_key(letter)
    stdscr.getch()
    for letter in "BOOOO!":
        terminal.proc_key(letter)
    stdscr.getch()

def textbox_test(stdscr: window):

    text = "This is a test to see the effectiveness of the textbox widget. How well is it working? You tell me. Or don't tell me. I can do my own testing and determining..."

    textbox = TextBox(4, 60, 2, 30)
    textbox.set_text(text)

    textbox.set_align(Align.RIGHT)
    textbox.read("CHAR")

    stdscr.getch()
    textbox.set_align(Align.LEFT)
    textbox.read("CHAR", 0.005)

    stdscr.getch()
    textbox.set_align(Align.CENTER)
    textbox.read("WORD", 0.002)

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

if __name__ == "__main__":
    curses.wrapper(main)