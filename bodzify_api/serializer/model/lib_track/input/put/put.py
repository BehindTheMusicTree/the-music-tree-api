
from typing import Any
from rest_framework import serializers

from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.serializer.PutSerializer import PutSerializer


class LibTrackPutSerializer(PutSerializer, LibTrackInputSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        print('PutSerializer.validate call')
        data = PutSerializer.validate(self, data)

        print('LibTrackInputSerializer.validate call')
        return super(LibTrackInputSerializer, self).validate(data)
