#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import \
    CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import \
    ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.AlbumWithoutTracksSerializer import \
    AlbumWithoutTracksSerializer
from bodzify_api.serializer.playlist.output.PlaylistWithoutTracksSerializer import \
    PlaylistWithoutTracksSerializer

class TrackDetailedSerializer(serializers.ModelSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    playlists = PlaylistWithoutTracksSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [
            ATTRIBUTES_LABEL.UUID,
            ATTRIBUTES_LABEL.RELATIVE_URL,
            ATTRIBUTES_LABEL.FILENAME,
            ATTRIBUTES_LABEL.FILE_EXTENSION,
            ATTRIBUTES_LABEL.FILE_EXISTS,
            ATTRIBUTES_LABEL.TITLE,
            ATTRIBUTES_LABEL.ARTIST,
            ATTRIBUTES_LABEL.ALBUM,
            ATTRIBUTES_LABEL.GENRE,
            ATTRIBUTES_LABEL.DURATION,
            ATTRIBUTES_LABEL.RATING,
            ATTRIBUTES_LABEL.LANGUAGE,
            ATTRIBUTES_LABEL.PLAYLISTS,
            ATTRIBUTES_LABEL.ADDED_ON]
