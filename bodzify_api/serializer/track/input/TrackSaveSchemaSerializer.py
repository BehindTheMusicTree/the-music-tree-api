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


class TrackSaveSchemaSerializer(InputSerializer):

    ATTRIBUTE_ARTIST_NAME_LABEL = "artistName"
    ATTRIBUTE_ALBUM_NAME_LABEL = "albumName"
    ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL = "albumArtistsName"
    ATTRIBUTE_GENRE_NAME_LABEL = "genreName"

    def validate(self, data):
        if self.ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL in data:
            if self.ATTRIBUTE_ALBUM_NAME_LABEL not in data:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
            elif data[self.ATTRIBUTE_ALBUM_NAME_LABEL] in [None, ""]:
                raise serializers.ValidationError(
                    ALBUM_ARTISTS_NAME_SET_BUT_NOT_ALBUM_NAME_ERROR_MESSAGE)
        return super().validate(data)
