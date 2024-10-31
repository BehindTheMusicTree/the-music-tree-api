
from rest_framework import serializers

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.artist.fields import Fields as AvailableFields
from bodzify_api.serializer.schema.album.minimum import AlbumMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    ALBUMS = AvailableFields.ALBUMS
    LIB_TRACKS_COUNT = AvailableFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = AvailableFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = AvailableFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC


class ArtistSimpleSerializer(serializers.ModelSerializer):
    albums = AlbumMinimumSerializer(many=True)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
