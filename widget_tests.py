import curses
from curses import window
from cursestools import consts as c
from cursestools import Panel, Terminal, Page, TextBox,\
    Dir, Align
from time import sleep
from random import randrange

def main(stdscr: window):
    curses.curs_set(2)
    stdscr.box()
    stdscr.noutrefresh()
    curses.doupdate()
    # print(repr(stdscr.getkey()))
    # raise SystemExit
    
    # textbox_test(stdscr)
    # panel_test(stdscr)
    # terminal_test(stdscr)
    page_test(stdscr)

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

    terminal = Terminal(3, 50, 2, 10, '> ')
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
    terminal.proc_key(c.ENTER)
    terminal_2 = Terminal(3, 30, 5, 70, "UNPROCESSED KEYS: ")
    for _ in range(20):
        terminal_2.proc_key(terminal.proc_key(terminal.getkey()))
    stdscr.getch()

def textbox_test(stdscr: window):

    text = "This is a test to see the effectiveness of the textbox widget. How well is it working? You tell me. Or don't tell me. I can do my own testing and determining..."
    textbox = TextBox(5, 60)
    textbox.set_text(text)

    textbox.print_textbox(stdscr, 7, 3)
    stdscr.getch()

    textbox.set_alignment(Align.RIGHT)
    textbox.read_textbox(stdscr, 7, 64, "CHAR", 0.01)
    stdscr.getch()

    textbox.set_alignment(Align.CENTER, v_centered=True)
    textbox.read_textbox(stdscr, 12, (stdscr.getmaxyx()[1] - 60) // 2, "WORD", 0.1)
    stdscr.getch()

def page_test(stdscr: window):
    ### FILLING CONTENT
    height, width = stdscr.getmaxyx()
    page = Page(stdscr, multiplier=2)
    for y in range(height * 2):
        for x in range(width * 2 - 1):
            num = randrange(32, 126)
            char = chr(num)
            page.addch(y, x, char)
    try:
        page.addch(height * 2, width * 2 - 1, char)
    except curses.error:
        pass
    page.refresh()

    binds = {'a': Dir.RIGHT, 's': Dir.UP, 'w': Dir.DOWN, 'd': Dir.LEFT}
    for _ in range(20):
        page.shift(binds.get(page.getkey(), Dir.LEFT))
        page.refresh()

if __name__ == "__main__":
    curses.wrapper(main)