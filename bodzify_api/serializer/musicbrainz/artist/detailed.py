#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist, ATTRIBUTES_LABEL


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    MUSICBRAINZ_LINK = ATTRIBUTES_LABEL.MUSICBRAINZ_LINK


class MusicbrainzArtistDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicbrainzArtist
        fields = [FIELDS.UUID, FIELDS.NAME, FIELDS.MUSICBRAINZ_LINK]
