from rest_framework import serializers
from django.db import models

from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.lib_track_playlist_rel.output.without_lib_track_mixin \
    import Fields as LibTrackPositionRelFields
from bodzify_api.serializer.schema.track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer
from .Fields import Fields


class BasePlaylistDetailedSerializer(serializers.ModelSerializer):

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
                  Fields.LAST_TRACK_LIST_UPDATE_DATE,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]

    def to_representation(self, instance: BasePlaylist):
        representation = super().to_representation(instance)
        library_tracks: models.QuerySet[LibraryTrack] = instance.library_tracks.all()
        serialized_tracks = []
        for track in library_tracks:
            serialized_track = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(track).data
            lib_track_playlist_relation: LibTrackPlaylistRel
            lib_track_playlist_relation = track.lib_track_playlist_rels.filter(base_playlist=instance).first()
            position = lib_track_playlist_relation.position
            serialized_track[LibTrackPositionRelFields.POSITION] = position
            serialized_tracks.append(serialized_track)
        representation[Fields.LIB_TRACKS] = sorted(
            serialized_tracks, key=lambda x: x[LibTrackPositionRelFields.POSITION])
        return representation
