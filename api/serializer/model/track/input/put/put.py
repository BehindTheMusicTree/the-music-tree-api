
from typing import Any
from rest_framework import serializers

from api.serializer.field.AppBooleanField import AppBooleanField
from api.serializer.model.track.input.input import TrackInputSerializer
from api.serializer.PutSerializer import PutSerializer


class TrackPutSerializer(PutSerializer, TrackInputSerializer):
    archived = AppBooleanField(required=False)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        data = PutSerializer.validate(self, data)
        self._validate_album_fields_from_data(data)
        return TrackInputSerializer.validate(self, data)
