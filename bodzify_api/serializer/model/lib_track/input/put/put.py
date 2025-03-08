
from typing import Any
from rest_framework import serializers

from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.serializer.PutSerializer import PutSerializer


class LibTrackPutSerializer(PutSerializer, LibTrackInputSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        attrs = super(PutSerializer, self).validate(attrs)
        return super(LibTrackInputSerializer, self).validate(attrs)
