#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.musicbrainz.MusicbrainzArtist import Fields as ModelFields, MusicbrainzArtist


class Fields:
    MUSICBRAINZ_ID = ModelFields.MUSICBRAINZ_ID
    NAME = ModelFields.NAME
    MUSICBRAINZ_LINK = ModelFields.MUSICBRAINZ_LINK


class MusicbrainzArtistDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicbrainzArtist
        fields = [Fields.MUSICBRAINZ_ID, Fields.NAME, Fields.MUSICBRAINZ_LINK]
