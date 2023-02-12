#!/usr/bin/env python
from django.contrib.auth.models import User
import bodzify_api.service.ArtistService as ArtistService
from bodzify_api.model.Album import Album


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
    
    albumQueryset = Album.objects.filter(user=user, name=albumName)
    if artists is not None:
        for albumArtist in artists:
            albumQueryset = albumQueryset.filter(albumArtists__in=[albumArtist])
    else:
        albumQueryset.filter(albumArtists=None)

    if albumQueryset.count() == 0:
        album = Album.objects.create(user=user, name=albumName)
        if artists is not None:
            album.albumArtists.set(artists)
    else:
        album = albumQueryset.first()
    return album
