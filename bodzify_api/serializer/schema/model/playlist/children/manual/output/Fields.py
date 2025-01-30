from bodzify_api.serializer.schema.model.playlist.children.detailed import Fields as ChildPlaylistFields


class Fields:
    UUID = ChildPlaylistFields.UUID
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    UPDATED_ON = ChildPlaylistFields.UPDATED_ON
    LIB_TRACKS_NOT_ARCHIVED_INTERNAL = ChildPlaylistFields.LIB_TRACKS_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_PUBLIC = ChildPlaylistFields.LIB_TRACKS_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = ChildPlaylistFields.LIB_TRACKS_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = ChildPlaylistFields.LIB_TRACKS_COUNT_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = ChildPlaylistFields.LIB_TRACKS_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = ChildPlaylistFields.LIB_TRACKS_COUNT_PUBLIC
    DURATION_IN_SEC = ChildPlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlaylistFields.NAME
