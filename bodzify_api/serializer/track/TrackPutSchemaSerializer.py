#!/usr/bin/env python

from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers


class TrackPutSchemaSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    artistName = serializers.CharField(max_length=100)
    albumName = serializers.CharField(max_length=100)
    albumArtistsNames = serializers.CharField(max_length=100)
    genre = serializers.CharField(max_length=100)
    rating = serializers.IntegerField(
            default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    language = serializers.CharField(max_length=100)
