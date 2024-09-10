#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME


class ArtistWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = [FIELDS.UUID, FIELDS.NAME]
