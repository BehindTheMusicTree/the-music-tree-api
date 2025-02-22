
from rest_framework import serializers

from bodzify_api.serializer.model.lib_track.input.input import LibTrackInputSerializer
from bodzify_api.validator.TrackUrlValidator import validate_url


class LibTrackExtractSerializer(LibTrackInputSerializer):
    url = serializers.URLField(validators=[validate_url])
