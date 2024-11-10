from rest_framework import serializers

from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.serializer.schema.lib_track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer
from .Fields import Fields


class LibTrackPlaylistRelWithLibTrackAndPosition(serializers.ModelSerializer):
    library_track = LibTrackSimpleWithoutPlaylistAndAlbumSerializer()

    class Meta:
        model = LibTrackPlaylistRel
        fields = [Fields.LIB_TRACK,
                  Fields.POSITION,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
