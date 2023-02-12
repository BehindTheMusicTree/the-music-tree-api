#!/usr/bin/env python

from django.contrib.auth.models import User

from bodzify_api.model.Artist import Artist


def GetArtistFromNameAfterHavingEventuallyCreatedIt(user: User, artistName: str) -> Artist:
    if artistName is None or artistName == "":
        return None
    else:
        try:
            artist = Artist.objects.get(user=user, name=artistName)
        except Artist.DoesNotExist:
            artist = None

        if artist is not None:
            return artist
        else:
            return Artist.objects.create(user=user, name=artistName)
