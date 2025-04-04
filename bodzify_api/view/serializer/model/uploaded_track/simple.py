from rest_framework import serializers

from bodzify_api.model.lib_track.LibTrack import UploadedTrack
from bodzify_api.model.lib_track.Fields import Fields


class UploadedTrackSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedTrack
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.ARTIST,
            Fields.ALBUM,
            Fields.GENRE,
            Fields.TAG,
            Fields.DURATION_MS,
            Fields.CREATED_AT,
            Fields.UPDATED_AT,
        ]
