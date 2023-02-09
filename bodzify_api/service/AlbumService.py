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
    if albumName is None or albumName == "":
        return None
    else:
        if albumArtistsNames is not None:
            albumArtists = [ArtistService.GetArtistFromNameAfterHavingEventuallyCreatedIt(
                 user=user, artistName=artistName) for artistName in albumArtistsNames]
        else:
            albumArtists = None
        try:
            album = Album.objects.get(user=user, name=albumName)
        except Album.DoesNotExist:
            album = Album.objects.create(user=user, name=albumName)
        
        
        if albumArtists != None:
            album.albumArtists.set(albumArtists)
        
        return album
