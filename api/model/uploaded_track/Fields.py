from api.model.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields(PrivateUniqueResourceFields, TrackablePlayCountFields):
    TRACK_FILE_INTERNAL = "track_file"
    TRACK_FILE_PUBLIC = "file"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = "track_file_fingerprint_must_be_unique"
    TITLE = "title"
    FILE = "file"
    ARTISTS = "artists"
    ALBUM = "album"
    TRACK_NUMBER = "track_number"
    GENRE = "genre"
    RATING = "rating"
    PLAYLISTS = "playlists"
    UPLOADED_TRACK_PLAYLIST_RELS = "uploaded_track_playlist_rels"
    LANGUAGE = "language"
    PLAYLISTS_PUBLIC = "playlists"
    ARCHIVED = 'archived'
    RELATIVE_URL = "relative_url"
