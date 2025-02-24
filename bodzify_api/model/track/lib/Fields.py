from bodzify_api.model.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from bodzify_api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields(PrivateUniqueResourceFields, TrackablePlayCountFields):
    TRACK_FILE = "track_file"
    TRACK_FILE_PUBLIC = "file"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = "track_file_fingerprint_must_be_unique"
    TITLE = "title"
    ARTISTS = "artists"
    ALBUM = "album"
    TRACK_NUMBER = "track_number"
    GENRE = "genre"
    RATING = "rating"
    PLAYLISTS = "playlists"
    LIB_TRACK_PLAYLIST_RELS = "lib_track_playlist_rels"
    LANGUAGE = "language"
    ARCHIVED = 'archived'
    RELATIVE_URL = "relative_url"