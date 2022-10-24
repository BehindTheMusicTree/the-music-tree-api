#!/usr/bin/env python

import os

from mutagen.easyid3 import EasyID3

import bodzify_api.api.settings as apiSettings
from bodzify_api.models import LibrarySong

def get(uuid):
    
    return LibrarySong.objects.get(uuid=uuid)

def delete(uuid):

    song = LibrarySong.objects.get(uuid=uuid)
    os.remove(song.path)
    song.delete()

def update(uuid, title, artist, album, genre, rating, language):

    song = LibrarySong.objects.get(uuid=uuid)
    song.title=title
    song.artist=artist
    song.album=album
    song.genre=genre
    song.rating=rating
    song.language=language
    song.save()

    songFile = EasyID3(song.path)

    if title is None:
        title = ""
    songFile[apiSettings.ID3_TAG_TITLE] = title
    if artist is None:
        artist = ""
    songFile[apiSettings.ID3_TAG_ARTIST] = artist
    if album is None:
        album = ""
    songFile[apiSettings.ID3_TAG_ALBUM] = album 
    if genre is None:
        genre = ""
    songFile[apiSettings.ID3_TAG_GENRE] = genre 
    if rating is None:
        rating = 0
    songFile[apiSettings.ID3_TAG_RATING] = str(rating)
    if language is None:
        language = ""
    songFile[apiSettings.ID3_TAG_LANGUAGE] = language
    songFile.save()

    return song