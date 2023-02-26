#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from upload_validator import FileTypeValidator
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.validator.LibraryTrackSizeValidator import validateTrackSize


class TrackSaveSchemaSerializer(InputSerializer):
    
        ATTRIBUTE_ARTIST_NAME_LABEL = "artistName"
        ATTRIBUTE_ALBUM_NAME_LABEL = "albumName"
        ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL = "albumArtistsNames"
        ATTRIBUTE_GENRE_NAME_LABEL = "genreName"


        file = serializers.FileField(
                help_text="Only audio formats accepted.", 
                validators=[
                        FileExtensionValidator(['flac', 'wav', 'mp3']), 
                        FileTypeValidator(allowed_types=[ 'audio/*']),
                        validateTrackSize], required=False)
        title = serializers.CharField(max_length=100, required=False)
        artistName = serializers.CharField(max_length=100, required=False)
        albumName = serializers.CharField(max_length=100, required=False)
        albumArtistsNames = serializers.CharField(max_length=100, required=False)
        genre = serializers.CharField(max_length=100, required=False)
        rating = serializers.IntegerField(
                default=0, 
                validators=[MinValueValidator(0), MaxValueValidator(255)], 
                required=False)
        language = serializers.CharField(max_length=100, required=False)
