#!/usr/bin/env python

from typing import Optional
from django.contrib.auth.models import User
from bodzify_api.model.Artist import Artist
from bodzify_api.model.Album import Album


def get_album_from_name_and_album_artists_name_list_after_eventual_creations(
        user: User, album_name: str, album_artists_name_list: list) -> Optional[Album]:
    
    if album_name is None or album_name == "":
        return None
    else:
        if album_artists_name_list is not None:
            if len(album_artists_name_list) > 0:
                album_artists = [Artist.get_artist_from_name_after_eventual_creation(
                    user=user, artist_name=artist_name) for artist_name in album_artists_name_list]
            else:
                album_artists = []
        else:
            album_artists = []
                
        return _get_album_from_name_and_artists_list_after_having_eventually_created_album(
                user=user, album_name=album_name, artists=album_artists)
    

def _get_album_from_name_and_artists_list_after_having_eventually_created_album(
        user: User, album_name: str, artists: list):
    
    album_queryset = Album.objects.filter(user=user, name=album_name)
    if len(artists) > 0:
        for albumArtist in artists:
            album_queryset = album_queryset.filter(album_artists__in=[albumArtist])
    else:
        album_queryset = album_queryset.filter(album_artists=None)

    if album_queryset.count() == 0:
        album = Album.objects.create(user=user, name=album_name)
        if artists is not None:
            album.album_artists.set(artists)
    else:
        album = album_queryset.first()
    return album
