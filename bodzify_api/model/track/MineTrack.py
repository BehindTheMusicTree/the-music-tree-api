#!/usr/bin/env python


class ATTRIBUTES_LABEL:
    URL = "url"


class MineTrack:
    def __init__(self, title: str, artistName: str, duration: float, releasedOn: str, url: str):
        self.title = title
        self.artistName = artistName
        self.duration = duration
        self.releasedOn = releasedOn
        self.url = url
