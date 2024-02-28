#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.playlist.output.PlaylistSerializer import PlaylistSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = ATTRIBUTES_LABEL.RELATIVE_URL
    FILENAME = ATTRIBUTES_LABEL.FILENAME
    FILE_EXTENSION = ATTRIBUTES_LABEL.FILE_EXTENSION
    FILE_EXISTS = ATTRIBUTES_LABEL.FILE_EXISTS
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    DURATION = ATTRIBUTES_LABEL.DURATION
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE
    PLAYLISTS = ATTRIBUTES_LABEL.PLAYLISTS
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    playlists = PlaylistSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.UUID,
                  FIELDS.RELATIVE_URL,
                  FIELDS.FILENAME,
                  FIELDS.FILE_EXTENSION,
                  FIELDS.FILE_EXISTS,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.DURATION,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.PLAYLISTS,
                  FIELDS.ADDED_ON]
