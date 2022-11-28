#!/usr/bin/env python

from django.db import models

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.criteria.Criteria import Criteria

class CriteriaPlaylist(Playlist):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = self.criteria.name