#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzArtist import MusicbrainzArtist, AttributesLabels


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    MUSICBRAINZ_LINK = AttributesLabels.MUSICBRAINZ_LINK


class MusicbrainzArtistDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicbrainzArtist
        fields = [Fields.UUID, Fields.NAME, Fields.MUSICBRAINZ_LINK]
