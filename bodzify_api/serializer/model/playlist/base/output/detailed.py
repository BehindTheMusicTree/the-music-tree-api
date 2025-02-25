from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.model.lib_track_playlist_rel.output.without_playlist import \
    LibTrackPlaylistRelWithoutPlaylist

from .Fields import Fields


class PlaylistDetailedSerializer(serializers.ModelSerializer):
    library_track_playlist_relations = LibTrackPlaylistRelWithoutPlaylist(
        source=Fields.LIB_TRACK_PLAYLIST_RELS_INTERNAL, many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL)
    type = AppCharField(source=Fields.TYPE_LABEL_INTERNAL)

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL_PUBLIC,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.LIB_TRACK_PLAYLIST_RELS_PUBLIC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.PLAY_COUNT,
                  Fields.LAST_TRACK_LIST_UPDATE_DATE,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
