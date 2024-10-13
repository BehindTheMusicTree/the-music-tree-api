#!/usr/bin/env python

from rest_framework import serializers
from django.db import models

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, AttributesLabels
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.type.detailed import CriteriaTypeSerializer
from bodzify_api.serializer.lib_track_playlist_position_rel.output.without_lib_track_mixin \
    import Fields as LibTrackPositionRelFields
from bodzify_api.serializer.track.output.simple_without_playlists_and_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    CREATED_ON = AttributesLabels.CREATED_ON
    UPDATED_ON = AttributesLabels.UPDATED_ON
    TYPE_LABEL = AttributesLabels.TYPE_LABEL
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = AttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = AttributesLabels.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = AttributesLabels.LAST_TRACK_LIST_UPDATE_DATE


class BasePlaylistWithTracksSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.PLAY_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.LAST_TRACK_LIST_UPDATE_DATE]

    def to_representation(self, instance: BasePlaylist):
        representation = super().to_representation(instance)
        library_tracks: models.QuerySet[LibraryTrack] = instance.library_tracks.all()
        serialized_tracks = []
        for track in library_tracks:
            serialized_track = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(track).data
            lib_track_playlist_relation: LibTrackPlaylistPositionRel
            lib_track_playlist_relation = track.lib_track_playlist_relations.filter(base_playlist=instance).first()
            position = lib_track_playlist_relation.position
            serialized_track[LibTrackPositionRelFields.POSITION] = position
            serialized_tracks.append(serialized_track)
        representation[Fields.LIB_TRACKS] = sorted(
            serialized_tracks, key=lambda x: x[LibTrackPositionRelFields.POSITION])
        return representation
