#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    TrackSaveSchemaSerializer
from bodzify_api.validator.MineTrackUrlValidator import validate_url

class ATTRIBUTES_LABEL:
    URL = "url"

class TrackExtractSchemaSerializer(TrackSaveSchemaSerializer):
    url = serializers.URLField(validators=[validate_url])

    class Meta(TrackSaveSchemaSerializer.Meta):
        fields = TrackSaveSchemaSerializer.Meta.fields + [ATTRIBUTES_LABEL.URL,]
