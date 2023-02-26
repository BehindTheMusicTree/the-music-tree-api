#!/usr/bin/env python
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from rest_framework import serializers
from bodzify_api.serializer.InputSerializer import InputSerializer
from bodzify_api.validator.MineTrackUrlValidator import validateUrl

class TrackExtractSchemaSerializer(InputSerializer):
    url = serializers.URLField(validators=[validateUrl])
    title = serializers.CharField(max_length=100)
    artistName = serializers.CharField(max_length=100, required=False)
    albumName = serializers.CharField(max_length=100, required=False)
    albumArtistsNames = serializers.CharField(max_length=100, required=False)
    genreName = serializers.CharField(max_length=100, required=False)
    rating = serializers.IntegerField(
            default=0, validators=[MinValueValidator(0), MaxValueValidator(255)], required=False)
    language = serializers.CharField(max_length=100, required=False)
    
    
    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise ValidationError("Unknown fields: {}".format(unknown_keys))
        return data
