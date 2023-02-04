#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Artist import Artist


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ['uuid', 'name']
