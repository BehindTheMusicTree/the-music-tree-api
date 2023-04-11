#!/usr/bin/env python
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from upload_validator import FileTypeValidator
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import (
    TrackSaveSchemaSerializer)
from bodzify_api.validator.LibraryTrackSizeValidator import validateTrackSize
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL


class TrackUpdateSchemaSerializer(TrackSaveSchemaSerializer):

    file = serializers.FileField(
        help_text="Only audio formats accepted.",
        validators=[
            FileExtensionValidator(['flac', 'wav', 'mp3']),
            FileTypeValidator(allowed_types=['audio/*']),
            validateTrackSize],
        required=False)

    class Meta(TrackSaveSchemaSerializer.Meta):
        fields = TrackSaveSchemaSerializer.Meta.fields + [ATTRIBUTES_LABEL.FILE,]
