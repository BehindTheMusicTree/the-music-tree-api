#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import Playlist

TYPE_GENRE = "genre"

class GenrePlaylist(Playlist):
    def __init__(self, genre):
        super(genre.name, TYPE_GENRE)
        self.genre = genre