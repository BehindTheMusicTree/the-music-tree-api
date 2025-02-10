from bodzify_api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields
from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields:
    UUID = LibTrackMixinFields.UUID
    USER = LibTrackMixinFields.USER
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    NAME_PUBLIC = LibTrackMixinFields.NAME_PUBLIC
    NAME_INTERNAL = LibTrackMixinFields.NAME_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_INTERNAL = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_PUBLIC = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC
    LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    LIB_TRACKS_ARCHIVED_COUNT_INTERNAL = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL
    LIB_TRACKS_ARCHIVED_COUNT_PUBLIC = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    LAST_TRACK_LIST_UPDATE_DATE = LibTrackMixinFields.LAST_TRACK_LIST_UPDATE_DATE

    PLAY_COUNT = TrackablePlayCountFields.PLAY_COUNT

    LIB_TRACKS_RELATED_NAME = 'lib_tracks_of_playlist'
    LIB_TRACK_PLAYLIST_RELS_INTERNAL = 'lib_track_playlist_rels'
    LIB_TRACK_PLAYLIST_RELS_PUBLIC = 'library_track_playlist_relations'
    TYPE_LABEL_INTERNAL = 'type_label'
    TYPE_LABEL_PUBLIC = 'type'
    PLAYLIST_LIB_TRACK_RELATIONS = 'lib_track_playlist_rels'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'
    MANUAL_PLAYLIST = 'manual_playlist'
    CRITERIA_PLAYLIST = 'criteria_playlist'
