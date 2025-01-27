
from bodzify_api.model.playlist.Fields import Fields as PlaylistFields
from bodzify_api.serializer.schema.model.playlist.base.output.simple import PlaylistSimpleSerializer


class Fields:
    UUID = PlaylistFields.UUID
    NAME = PlaylistFields.NAME_PUBLIC
    CREATED_ON = PlaylistFields.CREATED_ON
    UPDATED_ON = PlaylistFields.UPDATED_ON
    LIB_TRACKS = PlaylistFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = PlaylistFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = PlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED = PlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = PlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = PlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC


class ChildPlaylistSerializer(PlaylistSimpleSerializer):

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
