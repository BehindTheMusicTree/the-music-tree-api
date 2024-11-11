from bodzify_api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields
from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields:
    UUID = LibTrackMixinFields.UUID
    USER = LibTrackMixinFields.USER
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    NAME = LibTrackMixinFields.NAME
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = TrackablePlayCountFields.PLAY_COUNT
    LIB_TRACKS_RELATED_NAME = 'lib_tracks_of_playlist'
    LIB_TRACK_PLAYLIST_RELS = 'lib_track_playlist_rels'
    TYPE_LABEL = 'type_label'
    PLAYLIST_LIB_TRACK_RELATIONS = 'lib_track_playlist_rels'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'
    MANUAL_PLAYLIST = 'manual_playlist'
    CRITERIA_PLAYLIST = 'criteria_playlist'
