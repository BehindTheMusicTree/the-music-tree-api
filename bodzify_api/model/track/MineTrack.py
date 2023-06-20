#!/usr/bin/env python
class ATTRIBUTES_LABEL:
    TITLE = "title"
    ARTIST_NAME = "artist_name"
    DURATION = "duration"
    RELEASED_ON = "released_on"
    URL = "url"


class MineTrack:
    def __init__(self, title: str, artist_name: str, duration: float, released_on: str, url: str):
        self.title = title
        self.artist_name = artist_name
        self.duration = duration
        self.released_on = released_on
        self.url = url
