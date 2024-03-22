#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = ATTRIBUTES_LABEL.RELATIVE_URL
    FILENAME = ATTRIBUTES_LABEL.FILENAME
    FILE_EXTENSION = ATTRIBUTES_LABEL.FILE_EXTENSION
    FILE_EXISTS = ATTRIBUTES_LABEL.FILE_EXISTS
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    DURATION = ATTRIBUTES_LABEL.DURATION
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON


class LibTrackWithoutAlbumPlaylistGenreSerializer(serializers.ModelSerializer):
    artist = ArtistWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [
            FIELDS.UUID,
            FIELDS.RELATIVE_URL,
            FIELDS.FILENAME,
            FIELDS.FILE_EXTENSION,
            FIELDS.FILE_EXISTS,
            FIELDS.TITLE,
            FIELDS.ARTIST,
            FIELDS.DURATION,
            FIELDS.RATING,
            FIELDS.LANGUAGE,
            FIELDS.ADDED_ON]
