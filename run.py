#!/usr/bin/env python
from GrabSong import GrabSong


player = GrabSong("clementine")

print("Title: %s" % player.metadata["title"])
print("Artist: %s" % player.metadata["artist"])
print("Album: %s" % player.metadata["album"])
