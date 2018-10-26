#!/usr/bin/env python3
from subprocess import Popen
import os
import dbus
bus = dbus.SessionBus()

class GrabSong(object):
    def __init__(self, player):
        self.start = True
        self.player = player
        self.player_proper_name = None
        self.song_changed = True
        self.metadata = self.get_metadata()
        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.outdir = "%s/Output" % self.curdir
        self.outfiles = ["Artist", "Album", "Title"]
        self.song_art = None

    def get_metadata(self):
        data = bus.get_object("org.mpris.MediaPlayer2.%s" % self.player,
                      '/org/mpris/MediaPlayer2')

        interface = dbus.Interface(data, dbus_interface="org.freedesktop.DBus.Properties")
        metadata = interface.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        self.song_art = metadata["mpris:artUrl"]

        self.player_proper_name = interface.Get("org.mpris.MediaPlayer2", "Identity")

        returned_value = {
            "Artist": metadata["xesam:artist"][0],
            "Album": metadata["xesam:album"],
            "Title": metadata["xesam:title"]
        }

        if self.song_changed == False:
            self.song_changed = self.metadata["Artist"] != returned_value["Artist"] and self.metadata["Album"] != returned_value["Album"] and self.metadata["Title"] != returned_value["Title"]

        return returned_value

    def save(self):
        try:
            os.makedirs(self.outdir)
        except OSError:
            if os.path.isdir(self.outdir):
                pass
            else:
                raise

        for name in self.outfiles:
            with open("%s/Song%s.txt" % (self.outdir, name), "w") as f:
                f.write(self.metadata[name])
        if not self.song_art:
            self.song_art = "%s/Images/NoArt.jpg" % self.curdir

        Popen(
            [
                "convert",
                self.song_art, "-resize", "500x500!",
                self.outdir + "/AlbumArt.jpg"
            ]
        )

    def update(self):
        try:
            self.metadata = self.get_metadata()

            for typ in self.outfiles:
                try:
                    if self.metadata[typ]:
                        pass
                except KeyError:
                    self.metadata[typ] = "No information available."

            if self.song_changed or self.start is True:
                self.start = False
                self.song_changed = False
                self.save()
        except KeyError:
            self.metadata = "No valid metadata detected."
