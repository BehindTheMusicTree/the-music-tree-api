#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers


class TrackExtractSchemaSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=100, required=False)
    artistName = serializers.CharField(max_length=100, required=False)
    albumName = serializers.CharField(max_length=100, required=False)
    albumArtistsNames = serializers.CharField(max_length=100, required=False)
    genre = serializers.CharField(max_length=100, required=False)
    rating = serializers.IntegerField(
            default=0, validators=[MinValueValidator(0), MaxValueValidator(255)], required=False)
    language = serializers.CharField(max_length=100, required=False)
