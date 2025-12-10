from rest_framework import serializers

from api.model.playlist.Playlist import Playlist
from api.serializer.field.AppCharField import AppCharField
from api.serializer.model.track_playlist_rel.output.without_playlist import (
    TrackPlaylistRelWithoutPlaylist
)

from .Fields import Fields


class PlaylistDetailedSerializer(serializers.ModelSerializer):
    track_playlist_relations = TrackPlaylistRelWithoutPlaylist(
        source=Fields.TRACK_PLAYLIST_RELS_INTERNAL, many=True)
    tracks_count = serializers.IntegerField(source=Fields.TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    tracks_archived_count = serializers.IntegerField()
    type = AppCharField(source=Fields.TYPE_LABEL_INTERNAL)

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL_PUBLIC,
                  Fields.TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.TRACK_PLAYLIST_RELS_PUBLIC,
                  Fields.TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.PLAY_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
