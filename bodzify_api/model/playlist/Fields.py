from bodzify_api.model.uploaded_track_mixin.Fields import Fields as UploadedTrackMixinFields
from bodzify_api.model.uploaded_trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields(UploadedTrackMixinFields, TrackablePlayCountFields):
    UPLOADED_TRACKS_RELATED_NAME = 'uploaded_tracks_of_playlist'
    UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL = 'uploaded_track_playlist_rels'
    UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC = 'library_track_playlist_relations'
    TYPE_LABEL_INTERNAL = 'type_label'
    TYPE_LABEL_PUBLIC = 'type'
    PLAYLIST_UPLOADED_TRACK_RELATIONS = 'uploaded_track_playlist_rels'
    MANUAL_PLAYLIST = 'manual_playlist'
    CRITERIA_PLAYLIST = 'criteria_playlist'
