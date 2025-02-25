from bodzify_api.model.private_unique_resource.Fields import \
    Fields as PrivateResourceFields


class Fields:
    UUID = PrivateResourceFields.UUID
    USER = PrivateResourceFields.USER
    CREATED_ON = PrivateResourceFields.CREATED_ON
    UPDATED_ON = PrivateResourceFields.UPDATED_ON
    NAME_PUBLIC = 'name'
    NAME_INTERNAL = f'_{NAME_PUBLIC}'
    LIB_TRACKS_NOT_ARCHIVED_INTERNAL = 'lib_tracks_not_archived'
    LIB_TRACKS_NOT_ARCHIVED_PUBLIC = 'library_tracks'
    LIB_TRACKS_NOT_ARCHIVED_SORTED_INTERNAL = f'{LIB_TRACKS_NOT_ARCHIVED_INTERNAL}_sorted'
    LIB_TRACKS_NOT_ARCHIVED_SORTED_PUBLIC = f'{LIB_TRACKS_NOT_ARCHIVED_PUBLIC}_sorted'
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = f'{LIB_TRACKS_NOT_ARCHIVED_INTERNAL}_count'
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = f'{LIB_TRACKS_NOT_ARCHIVED_PUBLIC}_count'
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = 'lib_tracks_archived_count'
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = LIB_TRACKS_NOT_ARCHIVED_PUBLIC + '_archived_count'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'
