#!/usr/bin/env python
class MineTrack:

    ATTRIBUTE_URL_LABEL = "url"

    def __init__(self, title: str, artistName: str, duration: float, releasedOn: str, url: str):
        self.title = title
        self.artistName = artistName
        self.duration = duration
        self.releasedOn = releasedOn
        self.url = url