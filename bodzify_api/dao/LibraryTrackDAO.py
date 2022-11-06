#!/usr/bin/env python

import os

from mutagen.easyid3 import EasyID3

from bodzify_api.models import LibraryTrack

class LibraryDAO:
    def get(uuid):
        return LibraryTrack.objects.get(uuid=uuid)

    def getAllByUser(user):
        return LibraryTrack.objects.filter(user=user)

    def delete(uuid):
        track = LibraryTrack.objects.get(uuid=uuid)
        os.remove(track.path)
        track.delete()

    def update(uuid, title, artist, album, genre, rating, language):
        track = LibraryTrack.objects.get(uuid=uuid)
        track.title = title
        track.artist = artist
        track.album = album
        track.genre = genre
        track.rating = rating
        track.language = language
        track.save()

        trackFile = EasyID3(track.path)

        if title is None:
            title = ""
        trackFile[apiSettings.ID3_TAG_TITLE] = title
        if artist is None:
            artist = ""
        trackFile[apiSettings.ID3_TAG_ARTIST] = artist
        if album is None:
            album = ""
        trackFile[apiSettings.ID3_TAG_ALBUM] = album
        genreTag = ""
        if genre is not None:
            genreTag = genre.name
        trackFile[apiSettings.ID3_TAG_GENRE] = genreTag
        if rating is None:
            rating = -1
        trackFile[apiSettings.ID3_TAG_RATING] = str(rating)
        if language is None:
            language = ""
        trackFile[apiSettings.ID3_TAG_LANGUAGE] = language
        trackFile.save()

        return track