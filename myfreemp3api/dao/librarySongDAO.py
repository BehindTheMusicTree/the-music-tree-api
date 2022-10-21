#!/usr/bin/env python

import os

from mutagen.easyid3 import EasyID3

from myfreemp3api.serializers import SongDBSerializer

import myfreemp3api.api.settings as apiSettings
from myfreemp3api.models import SongDB

class LibrarySongDAO:

    def get(songDBUuid):
        
        return SongDB.objects.get(uuid=songDBUuid)

    def delete(songDBUuid):

        songDB = SongDB.objects.get(uuid=songDBUuid)
        os.remove(songDB.path)
        songDB.delete()

    def update(songUuid, title, artist, album, genre, rating, language):

        songDB = SongDB.objects.get(uuid=songUuid)
        songDB.title=title
        songDB.artist=artist
        songDB.album=album
        songDB.genre=genre
        songDB.rating=rating
        songDB.language=language
        songDB.save()

        songFile = EasyID3(songDB.path)

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

        return songDB