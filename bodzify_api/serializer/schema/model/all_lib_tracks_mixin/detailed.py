from rest_framework import serializers

from bodzify_api.model.all_lib_tracks_mixin.AllLibTracksMixin import AllLibTracksMixin
from bodzify_api.model.play import Fields
from bodzify_api.serializer.schema.model.lib_track.output.minimum import LibTrackMinimumSerializer
from .Fields import Fields


class AllLibTracksMixinDetailedSerializer(serializers.ModelSerializer):
    library_tracks = serializers.SerializerMethodField()

    class Meta:
        model = AllLibTracksMixin
        fields = [Fields.UUID,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,]

    def get_library_tracks(self, instance: AllLibTracksMixin):
        sorted_tracks = instance.lib_tracks_sorted
        return LibTrackMinimumSerializer(sorted_tracks, many=True).data
