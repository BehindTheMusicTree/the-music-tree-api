#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from upload_validator import FileTypeValidator
from bodzify_api.validator.LibraryTrackSizeValidator import trackSize


class TrackSaveSchemaSerializer(serializers.Serializer):
    
        ATTRIBUTE_FILE_LABEL = "file"
        ATTRIBUTE_TITLE_LABEL = "title"
        ATTRIBUTE_ARTIST_NAME_LABEL = "artistName"
        ATTRIBUTE_ALBUM_NAME_LABEL = "albumName"
        ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL = "albumArtistsNames"
        ATTRIBUTE_GENRE_NAME_LABEL = "genreName"
        ATTRIBUTE_RATING_LABEL = "rating"
        ATTRIBUTE_LANGUAGE_LABEL = "language"


        file = serializers.FileField(
                help_text="Only audio formats accepted.", 
                validators=[
                        FileExtensionValidator(['flac', 'wav', 'mp3']), 
                        FileTypeValidator(allowed_types=[ 'audio/*']),
                        trackSize],
                null=True)
        title = serializers.CharField(max_length=100)
        artistName = serializers.CharField(max_length=100)
        albumName = serializers.CharField(max_length=100)
        albumArtistsNames = serializers.CharField(max_length=100)
        genre = serializers.CharField(max_length=100)
        rating = serializers.IntegerField(
                default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
        language = serializers.CharField(max_length=100)
