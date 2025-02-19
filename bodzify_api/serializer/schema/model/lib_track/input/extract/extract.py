
from rest_framework import serializers

from bodzify_api.serializer.schema.model.lib_track.input.endpoint import LibTrackEndPointSerializer
from bodzify_api.validator.mine_track_validators import validate_url


class LibTrackExtractSerializer(LibTrackEndPointSerializer):
    url = serializers.URLField(validators=[validate_url])
