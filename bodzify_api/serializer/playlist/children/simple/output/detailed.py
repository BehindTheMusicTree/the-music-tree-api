#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.serializer.playlist.children.child import ChildPlaylistSerializer
from bodzify_api.serializer.playlist.children.child import Fields as ChildPlaylistFields
from bodzify_api.serializer.track.output.simple_without_playlists_and_album import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    UUID = ChildPlaylistFields.UUID
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    UPDATED_ON = ChildPlaylistFields.UPDATED_ON
    LIB_TRACKS = ChildPlaylistFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    NAME = ChildPlaylistFields.NAME


class SimplePlaylistDetailedSerializer(ChildPlaylistSerializer):
    name = serializers.CharField()  # Overriding the name field of the parent class
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(many=True)

    class Meta:
        model = SimplePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
