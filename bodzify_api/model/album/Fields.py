from bodzify_api.model.uploaded_track_mixin.Fields import Fields as UploadedTrackMixinFields


class Fields(UploadedTrackMixinFields):
    UPLOADED_TRACKS_RELATED_NAME = 'uploaded_tracks_of_album'
    YEAR = 'year'
    ALBUM_ARTISTS = 'album_artists'
