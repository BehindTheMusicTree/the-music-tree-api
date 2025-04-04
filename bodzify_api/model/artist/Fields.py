from bodzify_api.model.uploaded_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields(LibTrackMixinFields):
    UPLOADED_TRACKS_RELATED_NAME = 'uploaded_tracks_of_artist'
    ALBUMS = 'albums'
