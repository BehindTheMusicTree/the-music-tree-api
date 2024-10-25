#!/usr/bin/env python

from bodzify_api.model.base.PrivateUniqueResource import Fields as PrivateUniqueResourceFields
from bodzify_api.model.TrackablePlayCountModel import Fields as TrackablePlayCountFields


class Fields:
    MODEL = 'library_track'
    UUID = PrivateUniqueResourceFields.UUID
    USER = PrivateUniqueResourceFields.USER
    CREATED_ON = PrivateUniqueResourceFields.CREATED_ON
    UPDATED_ON = PrivateUniqueResourceFields.UPDATED_ON
    PLAY_COUNT = TrackablePlayCountFields.PLAY_COUNT
    TRACK_FILE_DB = "_track_file"
    TRACK_FILE_PROPERTY = "track_file"
    TRACK_FILE_USER_FRIENDLY = "file"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = "track_file_fingerprint_must_be_unique"
    TITLE = "title"
    ARTISTS = "artists"
    ALBUM = "album"
    POSITION_IN_ALBUM = "position_in_album"
    GENRE = "genre"
    RATING = "rating"
    BASE_PLAYLISTS = "base_playlists"
    BASE_PLAYLISTS_USER_FRIENDLY = "playlists"
    LANGUAGE = "language"
    ARCHIVED = 'archived'
    RELATIVE_URL = "relative_url"
