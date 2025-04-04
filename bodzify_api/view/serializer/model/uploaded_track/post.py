from rest_framework import serializers

from bodzify_api.model.lib_track.LibTrack import UploadedTrack
from bodzify_api.model.lib_track.Fields import Fields


class UploadedTrackPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedTrack
        fields = [
            Fields.NAME,
            Fields.ARTIST,
            Fields.ALBUM,
            Fields.GENRE,
            Fields.TAG,
            Fields.DURATION_MS,
            Fields.FILE_PATH,
        ]
        read_only_fields = [
            Fields.CREATED_AT,
            Fields.UPDATED_AT,
        ]

    def validate(self, data):
        if not data.get(Fields.NAME):
            raise serializers.ValidationError({Fields.NAME: "Name is required"})
        if not data.get(Fields.FILE_PATH):
            raise serializers.ValidationError({Fields.FILE_PATH: "File path is required"})
        return data
