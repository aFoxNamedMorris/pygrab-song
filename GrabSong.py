#!/usr/bin/env python
from subprocess import Popen, PIPE


class GrabSong(object):
    def __init__(self, player):
        self.player = player
        self.metadata = self.get_metadata(player)

    def get_metadata(self, player):
        data = Popen(["qdbus", "org.mpris.MediaPlayer2.%s" % player, "/org/mpris/MediaPlayer2", "org.mpris.MediaPlayer2.Player.Metadata"], stdout=PIPE)
        return self._parse_metadata(data)

    def _parse_metadata(self, data):
        data = data.stdout.read().decode("UTF-8")
        data = data.split("\n")
        data_dict = {}
        ignore = ["http", "url", "contentCreated"]

        for datum in data:
            if "xesam" in datum:
                d = datum[6:]  # get rid of "xesam:"
                d = d.split(":")
                if d[0] not in ignore:
                    data_dict[d[0]] = d[1]
                
        return data_dict

