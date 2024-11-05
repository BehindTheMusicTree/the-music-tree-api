
from bodzify_api.model.playlist.Fields import Fields as BasePlaylistFields
from bodzify_api.serializer.schema.playlist.base.output.simple import BasePlaylistSimpleSerializer


class Fields:
    UUID = BasePlaylistFields.UUID
    NAME = BasePlaylistFields.NAME
    CREATED_ON = BasePlaylistFields.CREATED_ON
    UPDATED_ON = BasePlaylistFields.UPDATED_ON
    LIB_TRACKS = BasePlaylistFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = BasePlaylistFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = BasePlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED = BasePlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = BasePlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = BasePlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = BasePlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC


class ChildPlaylistSerializer(BasePlaylistSimpleSerializer):

    class Meta:
        fields = [Fields.UUID,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
