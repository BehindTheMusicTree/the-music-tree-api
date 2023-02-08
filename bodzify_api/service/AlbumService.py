#!/usr/bin/env python

from django.contrib.auth.models import User

import bodzify_api.service.ArtistService as ArtistService
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


def DeleteAlbumIfNoTrackLinked(user: User, album: Album):
    if LibraryTrack.objects.filter(user=user, album=album).count() == 0:
        album.delete()


def GetAlbumFromNameAndAlbumArtistsNameAfterHavingEventuallyCreatedThem(
        user: User, albumName: str, albumArtistNames: list) -> Album:
    if albumName is None:
        return None
    else:
        albumArtists = []
        artistIndex = 0
        for artistName in albumArtistNames:
            albumArtists[artistIndex] = (
                    ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(artistName))
        try:
            album = Album.objects.get(user=user, name=albumName, albumArtists=albumArtists)
        except Album.DoesNotExist:
            album = None

        if album is not None:
            return album
        else:
            return Album.objects.create(user=user, name=albumName, albumArtists=albumArtists)
