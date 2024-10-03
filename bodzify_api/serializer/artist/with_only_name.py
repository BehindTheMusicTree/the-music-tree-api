#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.Artist import Artist, AttributesLabels


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME


class ArtistWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
