from bodzify_api.model.private_unique_resource.Fields import Fields as PrivateResourceFields


class Fields:
    UUID = PrivateResourceFields.UUID
    USER = PrivateResourceFields.USER
    CREATED_ON = PrivateResourceFields.CREATED_ON
    UPDATED_ON = PrivateResourceFields.UPDATED_ON
    NAME_PUBLIC = 'name'
    NAME_INTERNAL = f'_{NAME_PUBLIC}'
    LIB_TRACKS = 'library_tracks'
    LIB_TRACKS_NOT_ARCHIVED = LIB_TRACKS + '_not_archived'
    LIB_TRACKS_COUNT = LIB_TRACKS + '_count'
    LIB_TRACKS_ARCHIVED_COUNT = LIB_TRACKS + '_archived_count'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'
