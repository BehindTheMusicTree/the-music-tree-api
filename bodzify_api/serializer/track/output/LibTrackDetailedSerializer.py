#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.playlist.output.PlaylistSerializer import PlaylistSerializer


class FIELDS:
    UUID = LIB_TRACK_ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = LIB_TRACK_ATTRIBUTES_LABEL.RELATIVE_URL
    FILENAME = LIB_TRACK_ATTRIBUTES_LABEL.FILENAME
    FILE_EXTENSION = LIB_TRACK_ATTRIBUTES_LABEL.FILE_EXTENSION
    FILE_EXISTS = LIB_TRACK_ATTRIBUTES_LABEL.FILE_EXISTS
    TITLE = LIB_TRACK_ATTRIBUTES_LABEL.TITLE
    ARTIST = LIB_TRACK_ATTRIBUTES_LABEL.ARTIST
    ALBUM = LIB_TRACK_ATTRIBUTES_LABEL.ALBUM
    GENRE = LIB_TRACK_ATTRIBUTES_LABEL.GENRE
    DURATION = LIB_TRACK_ATTRIBUTES_LABEL.DURATION
    RATING = LIB_TRACK_ATTRIBUTES_LABEL.RATING
    LANGUAGE = LIB_TRACK_ATTRIBUTES_LABEL.LANGUAGE
    PLAYLISTS = LIB_TRACK_ATTRIBUTES_LABEL.PLAYLISTS
    ADDED_ON = LIB_TRACK_ATTRIBUTES_LABEL.ADDED_ON


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
