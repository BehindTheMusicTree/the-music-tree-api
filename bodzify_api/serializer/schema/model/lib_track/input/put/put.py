
from rest_framework import serializers

from bodzify_api.serializer.PutSerializer import PutSerializer
from bodzify_api.serializer.schema.model.lib_track.input.input import LibTrackInputSerializer


class LibTrackPutSerializer(PutSerializer, LibTrackInputSerializer):
    file = serializers.FileField(required=False)
    archived = serializers.BooleanField(required=False)
