from api.model.uploaded_track_mixin.Fields import Fields as UploadedTrackMixinFields
from api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields(UploadedTrackMixinFields, TrackablePlayCountFields):
    TRACKS_RELATED_NAME = 'tracks_of_playlist'
    TRACK_PLAYLIST_RELS_INTERNAL = 'track_playlist_rels'
    TRACK_PLAYLIST_RELS_PUBLIC = 'track_playlist_relations'
    TYPE_LABEL_INTERNAL = 'type_label'
    TYPE_LABEL_PUBLIC = 'type'
    PLAYLIST_TRACK_RELATIONS = 'track_playlist_rels'
    MANUAL_PLAYLIST = 'manual_playlist'
    CRITERIA_PLAYLIST = 'criteria_playlist'
