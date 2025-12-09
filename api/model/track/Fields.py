from api.model.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields(PrivateUniqueResourceFields, TrackablePlayCountFields):
    TITLE = "title"
    ARTISTS = "artists"
    ALBUM = "album"
    TRACK_NUMBER = "track_number"
    GENRE = "genre"
    RATING = "rating"
    PLAYLISTS = "playlists"
    TRACK_PLAYLIST_RELS = "track_playlist_rels"
    LANGUAGE = "language"
    PLAYLISTS_PUBLIC = "playlists"
    RELATIVE_URL = "relative_url"
