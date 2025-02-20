
from rest_framework import serializers

from bodzify_api.serializer.schema.model.lib_track.input.input import LibTrackInputSerializer


class LibTrackPostSerializer(LibTrackInputSerializer):
    file = serializers.FileField(required=True)
