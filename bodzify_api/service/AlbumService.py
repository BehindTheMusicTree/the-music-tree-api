#!/usr/bin/env python

from django.contrib.auth.models import User

import bodzify_api.service.ArtistService as ArtistService
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


def DeleteAlbumIfNoTrackLinked(user: User, album: Album):
    if LibraryTrack.objects.filter(user=user, album=album).count() == 0:
        album.delete()


def GetAlbumFromNameAndAlbumArtistsNamesAfterHavingEventuallyCreatedThem(
        user: User, albumName: str, albumArtistsNames: list) -> Album:
    if albumName is None:
        return None
    else:
        albumArtists = [ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
                user=user, artistName=artistName) for artistName in albumArtistsNames]
        try:
            album = Album.objects.get(user=user, name=albumName, albumArtists=albumArtists)
        except Album.DoesNotExist:
            album = Album.objects.create(user=user, name=albumName)
            album.albumArtists.set(albumArtists)
        
        return album
