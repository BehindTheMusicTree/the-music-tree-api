#!/usr/bin/env python

from django.contrib.auth.models import User
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.model.criteria.Criteria import Criteria


class GenreService:
    def createLinkedPlaylist(self, user: User, criteria: Criteria):
        GenrePlaylist(user=user, criteria=criteria).save()
