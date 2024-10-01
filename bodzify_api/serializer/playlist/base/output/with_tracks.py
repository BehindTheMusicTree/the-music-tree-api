#!/usr/bin/env python

from bodzify_api.model.playlist.BasePlaylist import AttributesLabel, BasePlaylist
from bodzify_api.serializer.playlist.base.output.without_tracks \
    import BasePlaylistWithoutTracksSerializer, Fields as ParentFields
from bodzify_api.serializer.playlist_lib_track_relation.output.without_playlist \
    import PlaylistLibTrackRelationWithoutPlaylist, Fields as PlaylistLibTrackRelFields
from rest_framework import serializers


class Fields:
    UUID = ParentFields.UUID
    NAME = ParentFields.NAME
    TYPE = ParentFields.TYPE
    CREATED_ON = ParentFields.CREATED_ON
    LIB_TRACKS_COUNT = ParentFields.LIB_TRACKS_COUNT
    LIB_TRACKS = AttributesLabel.LIB_TRACKS
    PLAY_COUNT = AttributesLabel.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = AttributesLabel.LAST_TRACK_LIST_UPDATE_DATE


class BasePlaylistWithTracksSerializer(BasePlaylistWithoutTracksSerializer):
    library_tracks = PlaylistLibTrackRelationWithoutPlaylist(
        source=AttributesLabel.PLAYLIST_LIB_TRACK_RELATIONS, many=True)
    library_tracks_count = serializers.IntegerField(source=f'{Fields.LIB_TRACKS}.count', read_only=True)

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.PLAY_COUNT,
                  Fields.LAST_TRACK_LIST_UPDATE_DATE]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation[Fields.LIB_TRACKS] = sorted(
            representation[Fields.LIB_TRACKS], key=lambda x: x[PlaylistLibTrackRelFields.POSITION])
        return representation
