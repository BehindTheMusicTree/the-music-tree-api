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

ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE = """Album name must be 
        specified if album artists name is."""


class TrackUpdateSchemaSerializer(InputSerializer):
    
        ATTRIBUTE_ARTIST_NAME_LABEL = "artistName"
        ATTRIBUTE_ALBUM_NAME_LABEL = "albumName"
        ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL = "albumArtistsName"
        ATTRIBUTE_GENRE_NAME_LABEL = "genreName"


        file = serializers.FileField(
                help_text="Only audio formats accepted.", 
                validators=[
                        FileExtensionValidator(['flac', 'wav', 'mp3']), 
                        FileTypeValidator(allowed_types=[ 'audio/*']),
                        validateTrackSize], 
                required=False)
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
        language = serializers.CharField(max_length=100, required=False, allow_blank=True)


        def validate(self, data):
                if self.ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL in data:
                        if self.ATTRIBUTE_ALBUM_NAME_LABEL not in data:
                                raise serializers.ValidationError(
                                        ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
                        elif data[self.ATTRIBUTE_ALBUM_NAME_LABEL] == "":
                                raise serializers.ValidationError(
                                        ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
                return super().validate(data)