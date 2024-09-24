#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.Artist import Artist, AttributesLabel


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME


class ArtistWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
