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
                
        return GetAlbumFromNameAndArtistsListAfterHavingEventuallyCreatedTheAlbum(
                user=user, albumName=albumName, artists=albumArtists)
    

def GetAlbumFromNameAndArtistsListAfterHavingEventuallyCreatedTheAlbum(
        user: User, albumName: str, artists: list):
    
    album = Album.objects.get(user=user, name=albumName)
    for albumArtist in artists:
        albumQueryset = albumQueryset.filter(albumArtists__in=[albumArtist])
    if albumQueryset.count() == 0:
        album = Album.objects.create(user=user, name=albumName)
        album.albumArtists.set(artists)
    else:
        album = albumQueryset.first()
    return album
