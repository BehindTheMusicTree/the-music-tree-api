from api.model.private_unique_resource.Fields import Fields as PrivateResourceFields


class Fields(PrivateResourceFields):
    NAME_PUBLIC = 'name'
    NAME_INTERNAL = f'_{NAME_PUBLIC}'
    TRACKS_NOT_ARCHIVED_INTERNAL = 'tracks_not_archived'
    TRACKS_NOT_ARCHIVED_PUBLIC = 'tracks'
    TRACKS_NOT_ARCHIVED_SORTED_INTERNAL = f'{TRACKS_NOT_ARCHIVED_INTERNAL}_sorted'
    TRACKS_NOT_ARCHIVED_SORTED_PUBLIC = f'{TRACKS_NOT_ARCHIVED_PUBLIC}_sorted'
    TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = f'{TRACKS_NOT_ARCHIVED_INTERNAL}_count'
    TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = f'{TRACKS_NOT_ARCHIVED_PUBLIC}_count'
    TRACKS_ARCHIVED_COUNT_INTERNAL = 'tracks_archived_count'
    TRACKS_ARCHIVED_COUNT_PUBLIC = TRACKS_NOT_ARCHIVED_PUBLIC + '_archived_count'
    DURATION_IN_SEC = 'duration_in_sec'
    DURATION_STR_IN_HOUR_MIN_SEC = 'duration_str_in_hour_min_sec'
