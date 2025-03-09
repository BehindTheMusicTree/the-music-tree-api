
from typing import Any
from rest_framework import serializers

from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.serializer.PutSerializer import PutSerializer


class LibTrackPutSerializer(PutSerializer, LibTrackInputSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        self._validate_album_fields_from_data(data)
        data = PutSerializer.validate(self, data)
        return super(LibTrackInputSerializer, self).validate(data)
