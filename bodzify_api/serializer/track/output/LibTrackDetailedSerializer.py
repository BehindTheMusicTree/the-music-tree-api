#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer import PlaylistWithoutTrackSerializer
from bodzify_api.serializer.file.output.FileDetailedSerializer import FileDetailedSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = ATTRIBUTES_LABEL.RELATIVE_URL
    FILE = 'file'
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    GENRE = ATTRIBUTES_LABEL.GENRE
    DURATION = ATTRIBUTES_LABEL.DURATION
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE
    PLAYLISTS = ATTRIBUTES_LABEL.PLAYLISTS
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    PLAY_COUNT = ATTRIBUTES_LABEL.PLAY_COUNT


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    genre = CriteriaSimpleSerializer()
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    playlists = PlaylistWithoutTrackSerializer(many=True)
    file = FileDetailedSerializer(source=ATTRIBUTES_LABEL.FILE_OBJ)

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.UUID,
                  FIELDS.RELATIVE_URL,
                  FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.ALBUM,
                  FIELDS.GENRE,
                  FIELDS.DURATION,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.PLAYLISTS,
                  FIELDS.ADDED_ON,
                  FIELDS.PLAY_COUNT]
