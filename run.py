#!/usr/bin/env python3
from GrabSong import GrabSong
import curses
import locale
from time import time, sleep

# Add these to a config file
debug = False
version = "0.0.5"
locale.setlocale(locale.LC_ALL, "")
# End Add these to a config file

player = GrabSong("pithos")

# Time until song information is updated
info_update_time = 0.5

# Minimum time between screen refreshes
min_update_time = 1.0/15.0

# Time since last update
last_update_time = 0

# Current status
status = None

# Current screen size
size = None

def validate():
    valid = ["Title", "Artist", "Album"]
    for v in valid:
        if type(v) is str:
            player.metadata[valid] = "Invalid metadata."

def set_strings(screen):
    global status
    global last_update_time
    global min_update_time
    global size

    last_update_time = last_update_time + min_update_time
    current_size = screen.getmaxyx()

    force_update = False

    if status is None or last_update_time > info_update_time:
        status = player.update()
        force_update = True
        last_update_time = 0

    if size is None or current_size != size:
        size = current_size
        force_update = True
        screen.redrawwin()

    if force_update == False:
        return

    screen.erase()

    title_x = 2
    title_y = 1

    if size[0] <= 2:
        title_y = 0
        title_x = 0
    else:
        screen.border()

    if size[0] > 4:
        title_y = 3
        try:
            screen.addstr(1, 2, "pygrab-song %s" % version, curses.color_pair(1))
        except curses.error:
            pass

    if size[0] > 9:
        try:
            screen.addstr(size[0]-2, 2, "Media Player: %s" % player.player_proper_name, curses.color_pair(1))
        except curses.error:
            pass

    if type(status) is not str:
        # validate()
        if type(player.metadata) is not str:
            if size[0] > 0:
                try:
                    screen.addstr(title_y, title_x, "Title: %s" % player.metadata["Title"])
                except curses.error:
                    pass

            if size[0] > 6:
                try:
                    screen.addstr(5, 2, "Artist: %s" % player.metadata["Artist"])
                except curses.error:
                    pass

            if size[0] > 8:
                try:
                    screen.addstr(7, 2, "Album: %s" % player.metadata["Album"])
                except curses.error:
                    pass

        if debug and size[0] > 11:
            screen.addstr(9, 2, "[DEBUG] Time: %s" % time())
            screen.addstr(10, 2, "[DEBUG] %s" % player.song_art)
    else:
        screen.addstr(3, 2, "This track has invalid metadata.")

    screen.refresh()

def main(screen):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.curs_set(0)
    while True:
        global min_update_time
        sleep(min_update_time)
        set_strings(screen)
    curses.endwin()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except (KeyboardInterrupt, SystemExit):
        curses.endwin()
