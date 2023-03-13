#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from upload_validator import FileTypeValidator
from bodzify_api import settings
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.validator.LibraryTrackSizeValidator import validateTrackSize


class TrackPostSchemaSerializer(InputSerializer):

        file = serializers.FileField(
                help_text="Only audio formats accepted.", 
                validators=[
                        FileExtensionValidator(['flac', 'wav', 'mp3']), 
                        FileTypeValidator(allowed_types=[ 'audio/*']),
                        validateTrackSize], 
                required=True)
        title = serializers.CharField(
                max_length=settings.TRACK_TITLE_MAX_CHAR, required=False)
        artistName = serializers.CharField(max_length=100, required=False, allow_blank=True)
        albumName = serializers.CharField(max_length=100, required=False, allow_blank=True)
        albumArtistsName = serializers.CharField(max_length=100, required=False, allow_blank=True)
        genreName = serializers.CharField(max_length=100, required=False, allow_blank=True)
        rating = serializers.IntegerField(
                validators=[MinValueValidator(0), MaxValueValidator(255)], 
                required=False, 
                allow_null=True)
        language = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
