
from rest_framework import serializers

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel, Fields as ModelFields
from bodzify_api.serializer.schema.track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    LIB_TRACK = ModelFields.LIB_TRACK
    POSITION = ModelFields.POSITION


class LibTrackPlaylistPositionRelWithLibTrackAndPosition(serializers.ModelSerializer):
    library_track = LibTrackSimpleWithoutPlaylistAndAlbumSerializer()

    class Meta:
        model = LibTrackPlaylistPositionRel
        fields = [Fields.LIB_TRACK,
                  Fields.POSITION,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
