#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist, ATTRIBUTES_LABEL


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME


class MusicbrainzArtistDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicbrainzArtist
        fields = [FIELDS.UUID, FIELDS.NAME]
