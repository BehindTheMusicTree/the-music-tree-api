#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)

class TrackDetailedSerializer(serializers.ModelSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithoutTracksSerializer()
    playlists = PlaylistWithoutTracksSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [
            LibraryTrack.ATTRIBUTE_UUID_LABEL,
            'relativeUrl',
            'filename',
            'fileExtension',
            'fileExists',
            LibraryTrack.ATTRIBUTE_TITLE_LABEL,
            LibraryTrack.ATTRIBUTE_ARTIST_LABEL,
            LibraryTrack.ATTRIBUTE_ALBUM_LABEL,
            LibraryTrack.ATTRIBUTE_GENRE_LABEL,
            LibraryTrack.ATTRIBUTE_DURATION_LABEL,
            LibraryTrack.ATTRIBUTE_RATING_LABEL,
            LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL,
            'playlists',
            'addedOn']
