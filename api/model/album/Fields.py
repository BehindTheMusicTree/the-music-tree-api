from api.model.track_mixin.Fields import Fields as TrackMixinFields


class Fields(TrackMixinFields):
    TRACKS_RELATED_NAME = 'tracks_of_album'
    YEAR = 'year'
    ALBUM_ARTISTS = 'album_artists'
