from bodzify_api.model.base.TrackablePlayCountModel import Fields as TrackablePlayCountFields
from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields:
    MODEL = 'base_playlist'
    UUID = LibTrackMixinFields.UUID
    USER = LibTrackMixinFields.USER
    CREATED_ON = LibTrackMixinFields.CREATED_ON
    UPDATED_ON = LibTrackMixinFields.UPDATED_ON
    LIB_TRACKS = LibTrackMixinFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = LibTrackMixinFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = LibTrackMixinFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = LibTrackMixinFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = LibTrackMixinFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackMixinFields.DURATION_STR_IN_HOUR_MIN_SEC
    PLAY_COUNT = TrackablePlayCountFields.PLAY_COUNT
    OBJECT = 'object'
    OBJECT_PK = 'object_pk'
    CONTENT_TYPE = 'content_type'
    TYPE_LABEL = 'type_label'
    NAME = 'name'
    CRITERIA_CHILD_PLAYLIST = 'criteria_child_playlist'
    MANUAL_CHILD_PLAYLIST = 'manual_child_playlist'
    PLAYLIST_LIB_TRACK_RELATIONS = 'lib_track_position_relations'
    LAST_TRACK_LIST_UPDATE_DATE = 'last_track_list_update_date'
