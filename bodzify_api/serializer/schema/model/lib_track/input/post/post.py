
from rest_framework import serializers

from bodzify_api.serializer.schema.model.lib_track.input.endpoint import LibTrackEndPointSerializer


class LibTrackPostSerializer(LibTrackEndPointSerializer):
    file = serializers.FileField(required=True)
