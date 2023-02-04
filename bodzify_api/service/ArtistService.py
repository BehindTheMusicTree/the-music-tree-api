#!/usr/bin/env python

from django.contrib.auth.models import User

from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


def DeleteArtistIfNoTrackLinked(user: User, artist: Artist):
    if LibraryTrack.objects.filter(user=user, artist=artist).count() == 0:
        Artist.objects.delete(artist)


def GetArtistFromNameAfterHavingEventuallyCreatedIt(user: User, artistName: str) -> str:
    if artistName is None:
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
