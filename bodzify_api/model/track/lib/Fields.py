from bodzify_api.model.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from bodzify_api.model.trackable_play_count.Fields import Fields as TrackablePlayCountFields


class Fields:
    UUID = PrivateUniqueResourceFields.UUID
    USER = PrivateUniqueResourceFields.USER
    CREATED_ON = PrivateUniqueResourceFields.CREATED_ON
    UPDATED_ON = PrivateUniqueResourceFields.UPDATED_ON
    PLAY_COUNT = TrackablePlayCountFields.PLAY_COUNT
    TRACK_FILE = "track_file"
    TRACK_FILE_PUBLIC = "file"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = "track_file_fingerprint_must_be_unique"
    TITLE = "title"
    ARTISTS = "artists"
    ALBUM = "album"
    POSITION_IN_ALBUM = "position_in_album"
    GENRE = "genre"
    RATING = "rating"
    PLAYLISTS = "playlists"
    LIB_TRACK_PLAYLIST_RELS = "lib_track_playlist_rels"
    PLAYLISTS = "playlists"
    LANGUAGE = "language"
    ARCHIVED = 'archived'
    RELATIVE_URL = "relative_url"
