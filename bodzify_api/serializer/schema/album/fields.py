#!/usr/bin/env python

from bodzify_api.model.Album import Fields as ModelFields


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    UUID = ModelFields.UUID
    NAME = ModelFields.NAME
    YEAR = ModelFields.YEAR
    ALBUM_ARTISTS = ModelFields.ALBUM_ARTISTS
    LIB_TRACKS = ModelFields.LIB_TRACKS
    LIB_TRACKS_COUNT = ModelFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ModelFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ModelFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ModelFields.DURATION_STR_IN_HOUR_MIN_SEC
