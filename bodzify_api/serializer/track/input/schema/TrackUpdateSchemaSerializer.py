#!/usr/bin/env python
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from bodzify_api import settings
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import (
    TrackSaveSchemaSerializer)
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL
from bodzify_api.validator.TrackFileValidator import validate_content_type_is_audio, validate_size


class TrackUpdateSchemaSerializer(TrackSaveSchemaSerializer):

    file = serializers.FileField(
        help_text="Only audio formats accepted.",
        validators=[
            FileExtensionValidator(settings.TRACK_FILE_EXTENSIONS),
            validate_content_type_is_audio, 
            validate_size],
        required=False)

    class Meta(TrackSaveSchemaSerializer.Meta):
        fields = TrackSaveSchemaSerializer.Meta.fields + [ATTRIBUTES_LABEL.FILE,]
