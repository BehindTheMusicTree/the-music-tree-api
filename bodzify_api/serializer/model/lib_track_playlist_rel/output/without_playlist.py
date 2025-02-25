from rest_framework import serializers

from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import \
    LibTrackPlaylistRel
from bodzify_api.serializer.model.lib_track.output.minimum import \
    LibTrackMinimumSerializer

from .Fields import Fields


class LibTrackPlaylistRelWithoutPlaylist(serializers.ModelSerializer):
    library_track = LibTrackMinimumSerializer(source=Fields.LIB_TRACK_INTERNAL)

    class Meta:
        model = LibTrackPlaylistRel
        fields = [Fields.LIB_TRACK_PUBLIC, Fields.POSITION,]
