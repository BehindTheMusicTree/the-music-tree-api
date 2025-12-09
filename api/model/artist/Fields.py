from api.model.uploaded_track_mixin.Fields import Fields as UploadedTrackMixinFields


class Fields(UploadedTrackMixinFields):
    TRACKS_RELATED_NAME = 'tracks_of_artist'
    ALBUMS = 'albums'
