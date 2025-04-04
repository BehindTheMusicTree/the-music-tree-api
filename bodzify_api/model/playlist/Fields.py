from bodzify_api.model.uploaded_track_mixin.Fields import Fields as LibTrackMixinFields
from bodzify_api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields(LibTrackMixinFields, TrackablePlayCountFields):
    LIB_TRACKS_RELATED_NAME = 'uploaded_tracks_of_playlist'
    LIB_TRACK_PLAYLIST_RELS_INTERNAL = 'uploaded_track_playlist_rels'
    LIB_TRACK_PLAYLIST_RELS_PUBLIC = 'library_track_playlist_relations'
    TYPE_LABEL_INTERNAL = 'type_label'
    TYPE_LABEL_PUBLIC = 'type'
    PLAYLIST_LIB_TRACK_RELATIONS = 'uploaded_track_playlist_rels'
    MANUAL_PLAYLIST = 'manual_playlist'
    CRITERIA_PLAYLIST = 'criteria_playlist'
