#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.playlist.children.detailed import Fields as ChildPlaylistFields

from bodzify_api.serializer.schema.track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    UUID = ChildPlaylistFields.UUID
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    UPDATED_ON = ChildPlaylistFields.UPDATED_ON
    LIB_TRACKS = ChildPlaylistFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildPlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlaylistFields.NAME


class ManualPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(many=True)
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
