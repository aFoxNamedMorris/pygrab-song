#!/usr/bin/env python
from subprocess import Popen, PIPE
import os

class GrabSong(object):
    def __init__(self, player):
        self.start = True
        self.player = player
        self.metadata = self.get_metadata()
        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.outdir = "%s/Output" % self.curdir
        self.outfiles = ["artist", "album", "title"]
        self.song_art = None

    def get_metadata(self):
        data = Popen(
            [
                "qdbus",
                "org.mpris.MediaPlayer2.%s" % self.player,
                "/org/mpris/MediaPlayer2",
                "org.mpris.MediaPlayer2.Player.Metadata"
            ],
            stdout=PIPE
        )
        return self._parse_metadata(data)

    def save(self):
        try:
            os.makedirs(self.outdir)
        except OSError:
            if os.path.isdir(self.outdir):
                pass
            else:
                raise

        for name in self.outfiles:
            with open("%s/%s.txt" % (self.outdir, name), "w") as f:
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
            try:
                last = self.metadata["title"]
            except (TypeError, KeyError):
                last = None
            self.metadata = self.get_metadata()

            for typ in self.outfiles:
                try:
                    if self.metadata[typ]:
                        pass
                except KeyError:
                    self.metadata[typ] = "No information available."

            if last != self.metadata["title"] or self.start is True:
                self.start = False
                self.save()
        except KeyError:
            self.metadata = "No valid metadata detected."

    def _parse_metadata(self, data):
        data = data.stdout.read().decode("UTF-8")
        data = data.split("\n")
        data_dict = {}
        ignore = ["comment", "url", "contentCreated"]

        for datum in data:
            if "mpris:artUrl:" in datum:
                self.song_art = datum[14:]  # Removes "mpris:artUrl:"
#            else:
#                self.song_art = None
            if "xesam" in datum:
                d = datum[6:].split(":")  # Removes "xesam:"
                if d[0] not in ignore:
                    data_dict[d[0]] = d[1].strip().encode("utf-8")
                
        return data_dict

