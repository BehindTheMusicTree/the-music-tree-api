
from rest_framework import serializers

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.model.album.minimum import AlbumMinimumSerializer
from bodzify_api.serializer.model.artist.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME_PUBLIC
    ALBUMS = AvailableFields.ALBUMS
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = AvailableFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = AvailableFields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = AvailableFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = AvailableFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    CREATED_ON = AvailableFields.CREATED_ON


class ArtistSimpleSerializer(serializers.ModelSerializer):
    albums = AlbumMinimumSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON]
