#!/usr/bin/env python

class AttributesLabel:
    TITLE = "title"
    ARTIST_NAME = "artist_name"
    DURATION_IN_SEC = "duration_in_sec"
    DURATION_STR_IN_HOUR_MIN_SEC = "duration_str_in_hour_min_sec"
    RELEASED_ON = "released_on"
    URL = "url"


class MineTrack:
    def __init__(self, title: str, artist_name: str, duration_in_sec: int, released_on: str, url: str):
        self.title = title
        self.artist_name = artist_name
        self.duration_in_sec = duration_in_sec
        self.released_on = released_on
        self.url = url
