from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.schema.model.lib_track_playlist_rel.output.without_playlist \
    import LibTrackPlaylistRelWithoutPlaylist
from .Fields import Fields


class PlaylistDetailedSerializer(serializers.ModelSerializer):
    lib_track_playlist_rels = LibTrackPlaylistRelWithoutPlaylist(many=True)
    type = serializers.CharField(source=Fields.TYPE_LABEL_INTERNAL)

    class Meta:
        model = Playlist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE_LABEL_PUBLIC,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACK_PLAYLIST_RELS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.PLAY_COUNT,
                  Fields.LAST_TRACK_LIST_UPDATE_DATE,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
