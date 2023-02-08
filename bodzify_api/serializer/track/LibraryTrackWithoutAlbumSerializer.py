#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.CriteriaSerializer import CriteriaResponseSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)

class LibraryTrackWithoutAlbumSerializer(serializers.ModelSerializer):
    genre = CriteriaResponseSerializer()
    artist = ArtistWithOnlyNameSerializer()
    playlists = PlaylistWithoutTracksSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [
            'uuid',
            'relativeUrl',
            'filename',
            'fileExtension',
            'fileExists',
            'title',
            'artist',
            'genre',
            'duration',
            'rating',
            'language',
            'playlists',
            'addedOn']
