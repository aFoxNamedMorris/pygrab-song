#!/usr/bin/env python
from GrabSong import GrabSong
import curses
import locale
from time import time, sleep


# Add these to a config file
debug = False
version = "0.0.1"
interval = 1
locale.setlocale(locale.LC_ALL, "")
# End Add these to a config file

player = GrabSong("pithos")

def validate():
    valid = ["title", "artist", "album"]
    for v in valid:
        if type(v) is str:
            player.metadata[valid] = "Invalid metadata."

def set_strings(screen):
    status = player.update()
    screen.erase()
    screen.border(1)    
    screen.addstr(1, 2, "pygrab-song %s" % version, curses.color_pair(1))
    if type(status) is not str:
#        validate()
        if type(player.metadata) is not str:
            screen.addstr(3, 2, "Title: %s" % player.metadata["title"])
            screen.addstr(5, 2, "Artist: %s" % player.metadata["artist"])
            screen.addstr(7, 2, "Album: %s" % player.metadata["album"])
        else:
            screen.addstr(3, 2, player.metadata)
        if debug:
            screen.addstr(9, 2, "[DEBUG] Time: %s" % time())
            screen.addstr(10, 2, "[DEBUG] %s" % player.song_art)
    else:
        screen.addstr(3, 2, "This track has invalid metadata.")

    screen.refresh()

def main(screen):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    while True:
        sleep(interval)
        set_strings(screen)
    curses.endwin()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except (KeyboardInterrupt, SystemExit):
        curses.endwin()
