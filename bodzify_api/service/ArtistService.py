#!/usr/bin/env python
from django.contrib.auth.models import User
from bodzify_api.model.Artist import Artist


def get_artist_from_name_after_eventual_creation(user: User, artist_name: str) -> Artist:
    if artist_name is None or artist_name == "":
        return None
    else:
        try:
            artist = Artist.objects.get(user=user, name=artist_name)
        except Artist.DoesNotExist:
            artist = None

        if artist is not None:
            return artist
        else:
            return Artist.objects.create(user=user, name=artist_name)
