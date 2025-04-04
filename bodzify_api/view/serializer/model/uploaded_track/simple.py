from rest_framework import serializers

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.model.uploaded_track.Fields import Fields


class UploadedTrackSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedTrack
        fields = [
            Fields.UUID,
            Fields.TITLE,
            Fields.ARTISTS
        ]
