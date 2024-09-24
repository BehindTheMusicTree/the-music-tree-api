#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabel
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer import PlaylistWithoutTrackSerializer
from bodzify_api.serializer.file.output.FileDetailedSerializer import FileDetailedSerializer


class FIELDS:
    UUID = AttributesLabel.UUID
    RELATIVE_URL = AttributesLabel.RELATIVE_URL
    FILE = 'file'
    TITLE = AttributesLabel.TITLE
    ARTIST = AttributesLabel.ARTIST
    ALBUM = AttributesLabel.ALBUM
    GENRE = AttributesLabel.GENRE
    DURATION = AttributesLabel.DURATION
    RATING = AttributesLabel.RATING
    LANGUAGE = AttributesLabel.LANGUAGE
    PLAYLISTS = AttributesLabel.PLAYLISTS
    ADDED_ON = AttributesLabel.ADDED_ON
    PLAY_COUNT = AttributesLabel.PLAY_COUNT


class LibTrackDetailedSerializer(serializers.ModelSerializer):
    genre = CriteriaSimpleSerializer()
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    playlists = PlaylistWithoutTrackSerializer(many=True)
    file = FileDetailedSerializer(source=AttributesLabel.FILE_OBJ)

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
