from rest_framework import serializers

from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import     LibTrackPlaylistRel
from bodzify_api.serializer.model.playlist.base.output.minimum import     PlaylistMinimumSerializer

from .Fields import Fields


class LibTrackPlaylistRelWithoutLibTrack(serializers.ModelSerializer):
    playlist = PlaylistMinimumSerializer()

    class Meta:
        model = LibTrackPlaylistRel
        fields = [Fields.PLAYLIST,
                  Fields.POSITION]
