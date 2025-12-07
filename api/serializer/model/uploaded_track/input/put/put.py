
from typing import Any
from rest_framework import serializers

from api.serializer.field.AppBooleanField import AppBooleanField
from api.serializer.model.uploaded_track.input.input import UploadedTrackInputSerializer
from api.serializer.PutSerializer import PutSerializer


class UploadedTrackPutSerializer(PutSerializer, UploadedTrackInputSerializer):
    file = serializers.FileField(required=False)
    archived = AppBooleanField(required=False)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        data = PutSerializer.validate(self, data)
        self._validate_album_fields_from_data(data)
        return UploadedTrackInputSerializer.validate(self, data)
