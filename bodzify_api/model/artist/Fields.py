from bodzify_api.model.lib_track_mixin.Fields import Fields as LibTrackMixinFields


class Fields(LibTrackMixinFields):
    LIB_TRACKS_RELATED_NAME = 'lib_tracks_of_artist'
    ALBUMS = 'albums'
