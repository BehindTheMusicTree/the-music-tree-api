from rest_framework import serializers

from bodzify_api.model.uploaded_track.LibTrack import UploadedTrack
from bodzify_api.model.uploaded_track.Fields import Fields


class UploadedTrackPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedTrack
        fields = [
            Fields.NAME,
            Fields.ARTIST,
            Fields.ALBUM,
            Fields.GENRE,
            Fields.TAG,
            Fields.DURATION_MS,
        ]
        read_only_fields = [
            Fields.FILE_PATH,
            Fields.CREATED_AT,
            Fields.UPDATED_AT,
        ]

    def validate(self, data):
        if not data.get(Fields.NAME):
            raise serializers.ValidationError({Fields.NAME: "Name is required"})
        return data
