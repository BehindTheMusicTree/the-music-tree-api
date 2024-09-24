#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist, AttributesLabel


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    MUSICBRAINZ_LINK = AttributesLabel.MUSICBRAINZ_LINK


class MusicbrainzArtistDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicbrainzArtist
        fields = [Fields.UUID, Fields.NAME, Fields.MUSICBRAINZ_LINK]
