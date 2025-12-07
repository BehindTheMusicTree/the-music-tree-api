
from rest_framework import serializers

from api.model.artist.Artist import Artist
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.artist.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME_PUBLIC
    ALBUMS = AvailableFields.ALBUMS
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL = AvailableFields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = AvailableFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    CREATED_ON = AvailableFields.CREATED_ON


class ArtistSimpleSerializer(serializers.ModelSerializer):
    albums = AlbumMinimumSerializer(many=True)
    uploaded_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    uploaded_tracks_archived_count = serializers.IntegerField()

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CREATED_ON]
